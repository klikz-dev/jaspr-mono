from jaspr.apps.awsmedia.models import Media
from jaspr.apps.test_infrastructure.testcases import JasprTestCase


class TestJasprMedia(JasprTestCase):
    def setUp(self):
        super(TestJasprMedia, self).setUp()
        self.media1 = self.create_media(file_type="video")
        self.media2 = self.create_media(file_type="video")

    def test_can_retrieve_media(self):
        """Can I get both media files and verify they are there?"""

        names = []
        filefields = []
        media_qs = Media.objects.all()
        self.assertEqual(len(media_qs), 2)
        for media in media_qs:
            names.append(media.name)
            filefields.append(media.file_field)
        self.assertIn(self.media1.name, names)
        self.assertIn(self.media2.name, names)
        self.assertIn(self.media2.file_field, filefields)
        self.assertIn(self.media1.file_field, filefields)

    def test_can_edit_media(self):
        """Can a filefield be edited?"""
        media = Media.objects.all()[0]
        media.name = "Test1"
        media.save()
        media = Media.objects.get(id=media.id)
        self.assertEqual(media.name, "Test1")

    def test_can_add_media(self):
        """Can a filefield be added?"""
        temp_file_field = self.create_media(file_type="graphic").file_field
        media = Media()
        media.name = "My added media file"
        media.file_field = temp_file_field
        media.file_type = "graphic"
        media.save()

        media.refresh_from_db()
        self.assertEqual(media.file_field, temp_file_field)
