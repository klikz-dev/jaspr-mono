from unittest import mock

from django.core.files.base import ContentFile

from jaspr.apps.common.storages import MediaRootS3Boto3Storage
from jaspr.apps.test_infrastructure.testcases import JasprSimpleTestCase


class TestStorages(JasprSimpleTestCase):
    def setUp(self):
        super().setUp()
        self.storage = MediaRootS3Boto3Storage()
        self.storage._connections.connection = mock.MagicMock()

        # Mocking exists because otherwise test takes a very long time.
        self.storage.exists = mock.MagicMock()
        self.storage.exists.return_value = False

    def test_name_has_md5(self):
        """ Is MD5 hex appended to the name of a media file?"""
        name = "media_test.txt"
        content = ContentFile(b"content")
        response = self.storage.save(name, content)
        self.assertEqual(response, "media_test-9a0364b9e99bb480dd25e1f0284c8555.txt")
