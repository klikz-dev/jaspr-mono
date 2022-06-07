from django.core.files.base import ContentFile

from jaspr.apps.test_infrastructure.testcases import JasprTestCase


class TestMedia(JasprTestCase):
    def test_original_field_field_name_saved_before_hashing(self):
        # Create a Dummy File to ensure that we have at least 1 mock_file.txt in the media folder.
        self.create_media(name="Dummy File")

        media = self.create_media(name="Media Object to Test")
        self.assertEqual(media.file_field_original_name, "mock_file.txt")
        self.assertEqual(len(media.file_field.name), len("mock_file.txt") + 8)
