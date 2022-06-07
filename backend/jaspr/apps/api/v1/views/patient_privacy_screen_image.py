import logging

from django.db import transaction
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from ..permissions import (
    HasRecentHeartbeat,
    IsAuthenticated,
    IsInER,
    IsPatient,
    SatisfiesClinicIPWhitelistingFromPatient,
)
from jaspr.apps.kiosk.models import Encounter
from ..serializers import (
    PrivacyScreenImageSerializer,
    PrivacyScreenSelectedImageSerializer,
)
from .base import JasprBaseView

logger = logging.getLogger(__name__)


class PatientPrivacyScreenImagesView(JasprBaseView):
    """
    GET
        returns a list of id and image urls from PrivacyScreenImage model.
        [
            {"id": 1, "image":<url here>},
            {"id": 2, "image":<url here>},
        ]
    """

    permission_classes = (
        IsAuthenticated,
        IsPatient,
        IsInER,
        SatisfiesClinicIPWhitelistingFromPatient,
    )

    def get(self, request):
        # getting 3 images that were preset on the patient.
        images = self.request.user.patient.current_privacy_screen_images.all()
        serializer = PrivacyScreenImageSerializer(images, many=True)
        return Response(serializer.data)


class PatientPrivacyScreenImageView(JasprBaseView):
    """
    PATCH
        sets the image id of the unlock image for the patient
        { "privacy_screen_image": 1 }
    """

    permission_classes = (
        IsAuthenticated,
        IsPatient,
        IsInER,
        SatisfiesClinicIPWhitelistingFromPatient,
        HasRecentHeartbeat,
    )

    @transaction.atomic
    def patch(self, request: Request):
        # Save the user selected image
        encounter = (
            Encounter.objects.filter(pk=request.auth.jaspr_session.encounter.pk)
                .select_for_update()
                .get()
        )
        serializer = PrivacyScreenSelectedImageSerializer(
            encounter, data=self.request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
