from typing import List

import boto3
import botocore.exceptions
from django.conf import settings
from django.core.management import CommandError
from jaspr.apps.awsmedia.models import Media
from jaspr.apps.common.management.base import JasprBaseCommand


class Command(JasprBaseCommand):
    """Check transcoding jobs for completion for media."""

    help = __doc__

    def handle(self, *args, **kwargs):
        if len(args) != 0:
            raise CommandError("No arguments needed.")
        self.dispatch()

    def dispatch(self):
        """The main method to perform all of the checking for transcoding complete."""
        videos = self.get_videos_to_check()
        video_queue = self.build_queue(videos)
        for item in video_queue:
            self.video_ready(item)
        for audio_media in self.get_audio_to_check():
            self.audio_ready(audio_media)

    def get_videos_to_check(self) -> List[Media]:
        """Returns the criteria for Quickpick."""
        awaiting_transcode = {"file_type": "video", "transcode_status": "queued"}
        jaspr_qs = Media.objects.filter(**awaiting_transcode).order_by("id")
        return jaspr_qs

    def get_audio_to_check(self) -> List[Media]:
        """Returns a list of all audio media previously queued for transcoding."""
        awaiting_transcode = {"file_type": "audio", "transcode_status": "queued"}
        jaspr_qs = Media.objects.filter(**awaiting_transcode).order_by("id")
        return jaspr_qs

    def build_queue(self, videos: List[Media]) -> List[dict]:
        """Returns a queue (`list`) of video objects/dictionaries."""
        return [
            {
                "video_id": video.id,
                "file_field": video.file_field,
                "bucket": video.bucket,
                "file_prefix": video.file_prefix,
                # Could also use `_meta.model`, but opting to go with `__class__` for now.
                "model": video.__class__,
            }
            for video in videos
        ]

    def video_ready(self, item):
        """Checks to see if the a video is transcoded and then updates instance."""
        client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
        output_key_prefix = f"{item['file_field'].name[:-4]}/"

        try:
            client.head_object(
                Bucket=item["bucket"], Key=f"{output_key_prefix}index.mpd"
            )
            video = item["model"].objects.get(id=item["video_id"])
            video.fpm4_transcode = "%s/index.mpd" % output_key_prefix
            video.mp4_transcode = "%s/%s_720p_%s.mp4" % (
                output_key_prefix,
                item["file_prefix"],
                output_key_prefix[:-1],
            )
            video.hls_playlist = "%s/index.m3u8" % output_key_prefix
            video.dash_playlist = "%s/index.mpd" % output_key_prefix
            video.transcode_status = "completed"
            video.save()
            print(f"Found and saved video: {output_key_prefix}")
        except botocore.exceptions.ClientError as e:
            if not e.response.get("Error", {}).get("Code") == str(404):
                raise
            print(f"Video not ready yet: {output_key_prefix}")

    def audio_ready(self, audio_media: Media):
        """Checks to see if the an audio media is transcoded and then updates instance."""
        client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
        output_key_prefix = f"{audio_media.file_field.name[:-4]}/"

        try:
            client.head_object(
                Bucket=audio_media.bucket, Key=f"{output_key_prefix}index.mpd"
            )
            # This is the straight 128k mp3 file.
            audio_media.mp3_transcode = f"{output_key_prefix}/{audio_media.file_prefix}128k_{output_key_prefix[:-1]}.mp3"
            # This is a dash playlist of a dash supported 128k mp3 file (from amazon elastic transcoder).
            audio_media.dash_playlist = f"{output_key_prefix}/index.mpd"
            audio_media.transcode_status = "completed"
            audio_media.save()
            print(f"Found and saved audio: {output_key_prefix}")
        except botocore.exceptions.ClientError as e:
            if not e.response.get("Error", {}).get("Code") == str(404):
                raise
            print(f"Audio not ready yet: {output_key_prefix}")
