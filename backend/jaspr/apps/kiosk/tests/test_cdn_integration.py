from jaspr.apps.awsmedia.management.commands.transcode_media import Command
from jaspr.apps.awsmedia.models import Media
from jaspr.apps.test_infrastructure.testcases import JasprTestCase


class TestVideoResource(JasprTestCase):
    def setUp(self):
        super(TestVideoResource, self).setUp()

        # The management command class
        self.command = Command()

        # Create fake videos
        self.video1 = self.create_media(file_type="video")
        self.video2 = self.create_media(file_type="video")
        self.video3 = self.create_media(file_type="video")

    def test_videos_exist(self):
        """ Do videos exist with the status new? """
        videos = Media.objects.filter(file_type="video").order_by("id")
        video1 = Media.objects.get(id=self.video1.id)
        video2 = Media.objects.get(id=self.video2.id)
        video3 = Media.objects.get(id=self.video3.id)
        self.assertEqual(len(videos), 3)
        self.assertEqual(video1.transcode_status, "new")
        self.assertEqual(video2.transcode_status, "new")
        self.assertEqual(video3.transcode_status, "new")

    def test_command_get_all_new(self):
        """Do all new movies get picked up? """
        videos = self.command.get_videos_to_transcode()
        self.assertEqual(len(videos), 3)
        self.assertEqual(videos[0].transcode_status, "new")
        self.assertEqual(videos[1].transcode_status, "new")
        self.assertEqual(videos[2].transcode_status, "new")

    def test_command_get_only_new(self):
        """Do only new movies get picked up? """
        self.video1.transcode_status = "queued"
        self.video1.save()
        videos = self.command.get_videos_to_transcode()
        self.assertEqual(len(videos), 2)
        self.assertEqual(videos[0].transcode_status, "new")
        self.assertEqual(videos[1].transcode_status, "new")

    def test_command_build_queue(self):
        """Does the queue get built with the three films?"""
        data = self.command.get_videos_to_transcode()
        result = self.command.build_queue(data)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]["video_id"], self.video1.id)
        self.assertEqual(result[0]["video_name"], self.video1.name)
        self.assertEqual(result[0]["file_field"], self.video1.file_field)
        self.assertEqual(result[1]["video_id"], self.video2.id)
        self.assertEqual(result[1]["video_name"], self.video2.name)
        self.assertEqual(result[1]["file_field"], self.video2.file_field)
        self.assertEqual(result[2]["video_id"], self.video3.id)
        self.assertEqual(result[2]["video_name"], self.video3.name)
        self.assertEqual(result[2]["file_field"], self.video3.file_field)
