import secrets
import time

import logging
import jwt
import requests
from django.conf import settings
from functools import cached_property

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from django.db import models
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from cache_memoize import cache_memoize
from model_utils import Choices
from fernet_fields import EncryptedTextField
from jaspr.apps.common.models import JasprAbstractBaseModel

logger = logging.getLogger("EPIC")

# Workaround to deal with weak DH keys used at Allina
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL'


class EpicSettings(JasprAbstractBaseModel):
    STATUS = Choices("active")

    name = models.CharField(
        "Name",
        max_length=50,
        blank=False,
        null=False,
        help_text="Label for this Epic instance",
    )

    provider = models.CharField(
        "Provider",
        max_length=15,
        choices=Choices("Epic"),
        blank=True,
        help_text="EHR Vendor for Clinic",
    )

    private_key_pem = EncryptedTextField(
        "Private Key",
        blank=True,
        null=True,
    )

    iss_url = models.CharField("Root URL", max_length=255, blank=True)

    @cached_property
    def private_key(self):
        if self.private_key_pem:
            return serialization.load_pem_private_key(
                bytes(self.private_key_pem, 'utf-8'),
                password=None,
            )
        return None

    @cached_property
    def public_key(self):
        if self.private_key:
            return self.private_key.public_key()
        return None

    @cached_property
    def serialized_public_key(self):
        if self.public_key:
            return self.public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode("utf-8")
        return None

    @staticmethod
    @cache_memoize(3600, prefix="epic_iss")
    def get_metadata(iss):
        if iss is None:
            logger.exception("ISS url is not provided")
            return None

        url = f"{iss}/metadata"

        session = requests.Session()
        retries = Retry(total=3, backoff_factor=0.25)
        session.mount("https://", HTTPAdapter(max_retries=retries))

        try:
            response = session.get(url, headers={"Accept": "application/json+fhir"})
        except requests.exceptions.RequestException as e:
            logger.warning("Unable to fetch metadata from %s", iss,)
            raise e

        metadata = response.json()

        return metadata

    @staticmethod
    def get_authorize_url(iss):
        if iss is None:
            logger.exception("ISS url is not provided")
            return None

        try:
            metadata = EpicSettings.get_metadata(iss)
        except:
            return None

        security_extensions = metadata["rest"][0]["security"]["extension"][0][
            "extension"
        ]

        for extension in security_extensions:
            if extension["url"] == "authorize":
                return extension["valueUri"]

    @staticmethod
    def get_token_url(iss):
        if iss is None:
            logger.exception("ISS url is not provided")
            return None

        try:
            metadata = EpicSettings.get_metadata(iss)
        except:
            return None

        security_extensions = metadata["rest"][0]["security"]["extension"][0][
            "extension"
        ]

        for extension in security_extensions:
            if extension["url"] == "token":
                return extension["valueUri"]


    def get_access_token(self):
        private_key = self.private_key

        epoch_time = int(time.time())
        token_url = self.get_token_url(self.iss_url)
        if not token_url:
            logger.exception(f"Unable to get token urls from EPIC instance metadata for {self.iss_url}")
            raise Exception("Unable to generate access token")

        encoded_jwt = jwt.encode(
            {
                "iss": settings.EPIC_BACKEND_CLIENT_ID,
                "sub": settings.EPIC_BACKEND_CLIENT_ID,
                "aud": self.get_token_url(self.iss_url),
                "jti": secrets.token_urlsafe(16),
                "exp": epoch_time + (60 * 4),
                "nbf": epoch_time - 60,
                "iat": epoch_time,
            },
            private_key,
            algorithm="RS384",
        )

        payload = {
            "grant_type": "client_credentials",
            "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
            "client_assertion": encoded_jwt,
        }

        session = requests.Session()
        retries = Retry(total=3, backoff_factor=0.25)
        session.mount("https://", HTTPAdapter(max_retries=retries))

        try:
            response = requests.post(token_url, data=payload)
        except requests.exceptions.RequestException as e:
            logger.warning("Unable to fetch access token from %s for EPIC Settings (%s)", token_url, self.pk)
            raise e

        if response.status_code == 200:
            data = response.json()
            return data["access_token"]
        else:
            logger.info("Request for access token failed with status code %s", response.status_code)
            logger.info(response.text)

        raise Exception("Unable to generate access token")

    def save(self, *args, **kwargs):
        """Create a private key if one has not been set"""
        if not self.private_key_pem:
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
            )

            self.private_key_pem = private_key.private_bytes(
                serialization.Encoding.PEM,
                serialization.PrivateFormat.TraditionalOpenSSL,
                serialization.NoEncryption()
            ).decode("utf-8")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"({self.pk}) {self.name}"

    class Meta:
        verbose_name = "Epic Settings"
        verbose_name_plural = "Epic Settings"
