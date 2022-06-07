import json
from typing import List

import boto3
from django.conf import settings
from django.core.management import CommandError
from jaspr.apps.awsmedia.models import Media
from jaspr.apps.common.management.base import JasprBaseCommand


class Command(JasprBaseCommand):
    """Queue transcoding jobs for media."""

    help = __doc__

    def __init__(self):
        super().__init__()
        # creating client to access AWS S3
        self.s3_client = boto3.client(
            "s3",
            region_name="us-west-1",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
        # Creating client for accessing elastic transcoder
        self.transcoder_client = boto3.client(
            "elastictranscoder",
            region_name="us-west-2",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )

    def handle(self, *args, **options):
        if len(args) != 0:
            raise CommandError("No arguments should be provided/needed.")
        self.dispatch()

    def dispatch(self):
        """The main method to perform all of the transcoding."""
        videos = self.get_videos_to_transcode()
        video_queue = self.build_queue(videos)
        # Download one item at a time.
        for item in video_queue:
            # get video to update status
            video = item["model"].objects.get(id=item["video_id"])
            self.delete_existing_derived_files(video)
            # Dispatch the transcode job
            # It will skip if its in the above failure
            job_created_hls = self.hls_transcode(item)
            job_created_dash = self.dash_transcode(item)
            if job_created_hls and job_created_dash:
                video.transcode_status = "queued"
                video.save()
        for audio_media in self.get_audio_to_transcode():
            job_created_mp3 = self.mp3_transcode(audio_media)
            if job_created_mp3:
                audio_media.transcode_status = "queued"
                audio_media.save()

    def get_videos_to_transcode(self) -> List[Media]:
        """Returns the criteria for Quickpick."""
        awaiting_transcode = {"file_type": "video", "transcode_status": "new"}
        jaspr_qs = Media.objects.filter(**awaiting_transcode).order_by("id")
        return jaspr_qs

    def get_audio_to_transcode(self) -> List[Media]:
        """Returns a list of all audio media awaiting transcoding."""
        awaiting_transcode = {"file_type": "audio", "transcode_status": "new"}
        jaspr_qs = Media.objects.filter(**awaiting_transcode).order_by("id")
        return jaspr_qs

    def delete_existing_derived_files(self, video):
        """
        Delete the old files that are generated by the elastic transcoder.
        This will cause jobs to fail without it.
        """
        folder_name = f"{self.file_name(video.file_field)}/"
        response = self.s3_client.list_objects_v2(Bucket=video.bucket, Prefix=folder_name)
        print("delete existing derived files")
        print(response)
        if response is None or 'Contents' not in response:
            print("response is None or 'Contents' is key in response")
            return

        print("iterating through files")
        for item in response['Contents']:
            print(item['Key'])
            self.s3_client.delete_object(Bucket=video.bucket, Key=item['Key'])

    def build_queue(self, videos: List[Media]) -> List[dict]:
        """Returns a queue (`list`) of video objects/dictionaries."""
        return [
            {
                "video_id": video.id,
                "video_name": video.name,
                "file_field": video.file_field,
                # NOTE: This is not currently present on Jaspr, but was
                # present on iKinnect. At the time of coding, leaving it in in case
                # we add in `subtitle_file` to Jaspr.
                # (Convert the empty string or `None` to the empty string)
                "subtitle_file": getattr(video, "subtitle_file", None) or "",
                "pipeline_id": video.pipeline_id,
                "bucket": video.bucket,
                "file_prefix": video.file_prefix,
                # Could also use `_meta.model`, but opting to go with `__class__` for now.
                "model": video.__class__,
            }
            for video in videos
        ]

    def file_name(self, file_field):
        return str(file_field)[:-4]

    def hls_transcode(self, item):
        """
        http://docs.aws.amazon.com/elastictranscoder/latest/developerguide/sample-code.html#python-pipeline
        """
        file_prefix = item["file_prefix"]
        pipeline_id = item["pipeline_id"]

        # This is the name of the input key that you would like to transcode.
        input_key = "%s" % (item["file_field"])
        subtitle_key = "%s" % (item["subtitle_file"])

        # fpm4 Presets that will be used to create an adaptive bitrate playlist.
        hls_400k_preset_id = "1351620000001-200055"
        hls_600k_preset_id = "1351620000001-200045"
        hls_1000k_preset_id = "1351620000001-200035"
        hls_1500k_preset_id = "1351620000001-200025"
        hls_2000k_preset_id = "1351620000001-200015"
        hls_64k_audio_preset_id = "1351620000001-200071"
        hls_160k_audio_preset_id = "1351620000001-200060"

        segment_duration = "4"

        # All outputs will have this prefix prepended to their output key.
        file_name = self.file_name(item["file_field"])

        # Setup the job input using the provided input key.
        job_input = {"Key": input_key}

        hls_400k = {
            "Key": "%s400_%s.%s" % (file_prefix, file_name, "m3u8"),
            "PresetId": hls_400k_preset_id,
            "SegmentDuration": segment_duration,
        }
        hls_600k = {
            "Key": "%s600_%s.%s" % (file_prefix, file_name, "m3u8"),
            "PresetId": hls_600k_preset_id,
            "SegmentDuration": segment_duration,
        }
        hls_1000k = {
            "Key": "%s1000_%s.%s" % (file_prefix, file_name, "m3u8"),
            "PresetId": hls_1000k_preset_id,
            "SegmentDuration": segment_duration,
        }
        hls_1500k = {
            "Key": "%s1500_%s.%s" % (file_prefix, file_name, "m3u8"),
            "PresetId": hls_1500k_preset_id,
            "SegmentDuration": segment_duration,
        }
        hls_2000k = {
            "Key": "%s2000_%s.%s" % (file_prefix, file_name, "m3u8"),
            "PresetId": hls_2000k_preset_id,
            "SegmentDuration": segment_duration,
        }
        hls_64_audio = {
            "Key": "%s64_%s.%s" % (file_prefix, file_name, "m3u8"),
            "PresetId": hls_64k_audio_preset_id,
            "SegmentDuration": segment_duration,
        }
        hls_160_audio = {
            "Key": "%s160_%s.%s" % (file_prefix, file_name, "m3u8"),
            "PresetId": hls_160k_audio_preset_id,
            "SegmentDuration": segment_duration,
        }
        hls_job_outputs = [
            hls_400k,
            hls_600k,
            hls_1000k,
            hls_1500k,
            hls_2000k,
            hls_64_audio,
            hls_160_audio,
        ]
        if subtitle_key:
            caption_output = {
                "MergePolicy": "Override",
                "CaptionSources": [
                    {"Key": subtitle_key, "Language": "en", "Label": "English"}
                ],
                "CaptionFormats": [
                    {
                        "Format": "webvtt",
                        "Pattern": "%s_%s_%s_{language}"
                        % (file_prefix, file_name, "hls"),
                    }
                ],
            }
            for item in hls_job_outputs:
                item["Captions"] = caption_output

        # Setup master playlist which can be used to play using adaptive bitrate.
        hls_playlist = {
            "Name": "index",
            "Format": "HLSv4",
            "OutputKeys": [x["Key"] for x in hls_job_outputs],
        }

        # Creating fpm4 job.
        hls_create_job_request = {
            "PipelineId": pipeline_id,
            "Input": job_input,
            "OutputKeyPrefix": "%s/" % (file_name),
            "Outputs": hls_job_outputs,
            "Playlists": [hls_playlist],
        }
        hls_create_job_result = self.transcoder_client.create_job(**hls_create_job_request)
        for item in [hls_create_job_result]:
            print(
                "HLS job has been created: ",
                json.dumps(item["Job"], indent=4, sort_keys=True),
            )
        return [hls_create_job_result]

    def dash_transcode(self, item):
        """
        http://docs.aws.amazon.com/elastictranscoder/latest/developerguide/sample-code.html#python-pipeline
        """
        file_prefix = item["file_prefix"]
        pipeline_id = item["pipeline_id"]

        # This is the name of the input key that you would like to transcode.
        input_key = "%s" % (item["file_field"])
        subtitle_key = "%s" % (item["subtitle_file"])

        # Region where the sample will be run
        region = "us-west-2"

        # fpm4 Presets that will be used to create an adaptive bitrate playlist.
        fpm4_0600k_preset_id = "1588688338434-m7d5vn"
        fpm4_1500k_preset_id = "1588688387551-vyg984"
        fpm4_2400k_preset_id = "1588688438432-or9l93"
        fpm4_4800k_preset_id = "1588688475241-3kx0bw"
        fpm4_64k_audio_preset_id = "1588688543340-wwcb7d"
        generic_720p_preset_id = "1351620000001-000010"

        segment_duration = "4"

        # All outputs will have this prefix prepended to their output key.
        file_name = str(item["file_field"])[:-4]
        output_key_prefix = "%s/" % (file_name)

        # Setup the job input using the provided input key.
        job_input = {"Key": input_key}

        fpm4_600k = {
            "Key": "%s600_%s.%s" % (file_prefix, file_name, "fmp4"),
            "PresetId": fpm4_0600k_preset_id,
            "SegmentDuration": segment_duration,
        }
        fpm4_1500k = {
            "Key": "%s1500_%s.%s" % (file_prefix, file_name, "fmp4"),
            "PresetId": fpm4_1500k_preset_id,
            "SegmentDuration": segment_duration,
        }
        fpm4_2400k = {
            "Key": "%s2400_%s.%s" % (file_prefix, file_name, "fmp4"),
            "PresetId": fpm4_2400k_preset_id,
            "SegmentDuration": segment_duration,
        }
        fpm4_4800k = {
            "Key": "%s4800_%s.%s" % (file_prefix, file_name, "fmp4"),
            "PresetId": fpm4_4800k_preset_id,
            "SegmentDuration": segment_duration,
        }
        fpm4_audio = {
            "Key": "%smono_%s.%s" % (file_prefix, file_name, "fmp4"),
            "PresetId": fpm4_64k_audio_preset_id,
            "SegmentDuration": segment_duration,
        }
        mp4_720p = {
            "Key": "%s_720p_%s.%s" % (file_prefix, file_name, "mp4"),
            "PresetId": generic_720p_preset_id,
        }
        fpm4_job_outputs = [fpm4_600k, fpm4_1500k, fpm4_2400k, fpm4_4800k, fpm4_audio]

        mp4_job_outputs = [mp4_720p]

        if subtitle_key:
            caption_output = {
                "MergePolicy": "Override",
                "CaptionSources": [
                    {"Key": subtitle_key, "Language": "en", "Label": "English"}
                ],
                "CaptionFormats": [
                    {
                        "Format": "webvtt",
                        "Pattern": "%s_%s_%s_{language}"
                        % (file_prefix, file_name, "fpm4"),
                    }
                ],
            }
            for item in fpm4_job_outputs:
                item["Captions"] = caption_output

        # Setup master playlist which can be used to play using adaptive bitrate.
        fpm4_playlist = {
            "Name": "index",
            "Format": "MPEG-DASH",
            "OutputKeys": [x["Key"] for x in fpm4_job_outputs],
        }

        # Creating fpm4 job.
        fpm4_create_job_request = {
            "PipelineId": pipeline_id,
            "Input": job_input,
            "OutputKeyPrefix": output_key_prefix,
            "Outputs": fpm4_job_outputs,
            "Playlists": [fpm4_playlist],
        }
        # Creating mp4 job.
        mp4_create_job_request = {
            "PipelineId": pipeline_id,
            "Input": job_input,
            "OutputKeyPrefix": output_key_prefix,
            "Outputs": mp4_job_outputs,
            "Playlists": [],
        }
        fpm4_create_job_result = self.transcoder_client.create_job(**fpm4_create_job_request)
        mp4_create_job_result = self.transcoder_client.create_job(**mp4_create_job_request)
        for item in [fpm4_create_job_result, mp4_create_job_result]:
            print(
                "Dash job has been created: ",
                json.dumps(item["Job"], indent=4, sort_keys=True),
            )
        return [fpm4_create_job_result, mp4_create_job_result]

    def mp3_transcode(self, audio_media: Media):
        file_prefix = audio_media.file_prefix
        pipeline_id = audio_media.pipeline_id

        # This is the name of the input key that you would like to transcode.
        input_key = f"{audio_media.file_field}"  # Convert `file_field` to a string.

        # Region where the sample will be run.
        region = "us-west-2"

        # mp3 presets to use.
        mp3_128k_preset_id = "1351620000001-300040"
        # NOTE: Not using the presets below right now since I don't think
        # they can be used in a dash playlist because of the segment duration
        # not being able to be set for mp3s (for elastic transcoder).
        # mp3_160k_preset_id = '1351620000001-300030'
        # mp3_192k_preset_id = '1351620000001-300020'
        # mp3_320k_preset_id = '1351620000001-300010'

        # mpd (MPEG-DASH) presets that will be used to create an adaptive bitrate playlist.
        mpd_128k_audio_present_id = "1351620000001-500060"

        # All outputs will have this prefix prepended to their output key.
        file_name = f"{audio_media.file_field}"[:-4]
        output_key_prefix = f"{file_name}/"

        # Setup the job input using the provided input key.
        job_input = {"Key": input_key}

        mp3_128k = {
            "Key": f"{file_prefix}128k_{file_name}.mp3",
            "PresetId": mp3_128k_preset_id,
        }
        # mp3_160k = {
        #     'Key': f"{file_prefix}160k_{file_name}.mp3",
        #     'PresetId': mp3_160k_preset_id,
        # }
        # mp3_192k = {
        #     'Key': f"{file_prefix}192k_{file_name}.mp3",
        #     'PresetId': mp3_192k_preset_id,
        # }
        # mp3_320k = {
        #     'Key': f"{file_prefix}320k_{file_name}.mp3",
        #     'PresetId': mp3_320k_preset_id,
        # }

        mp3_job_outputs = [mp3_128k]
        # mp3_job_outputs = [mp3_128k, mp3_160k, mp3_192k, mp3_320k]

        segment_duration = "4"

        mpd_128k = {
            "Key": f"{file_prefix}mpd128k_{file_name}.mp3",
            "PresetId": mpd_128k_audio_present_id,
            "SegmentDuration": segment_duration,
        }

        mpd_job_outputs = [mpd_128k]

        # Setup master playlist which can be used to play using adaptive bitrate.
        mpd_playlist = {
            "Name": "index",
            "Format": "MPEG-DASH",
            "OutputKeys": [x["Key"] for x in mpd_job_outputs],
        }

        # Creating mp3 job.
        mp3_create_job_request = {
            "PipelineId": pipeline_id,
            "Input": job_input,
            "OutputKeyPrefix": output_key_prefix,
            "Outputs": mp3_job_outputs,
            "Playlists": [],
        }

        # Creating mpd job.
        mpd_create_job_request = {
            "PipelineId": pipeline_id,
            "Input": job_input,
            "OutputKeyPrefix": output_key_prefix,
            "Outputs": mpd_job_outputs,
            "Playlists": [mpd_playlist],
        }

        mp3_create_job_result = self.transcoder_client.create_job(**mp3_create_job_request)
        mpd_create_job_result = self.transcoder_client.create_job(**mpd_create_job_request)
        for result, print_str in [
            (mp3_create_job_result, "MP3"),
            (mpd_create_job_result, "MPEG-DASH"),
        ]:
            print(
                f"(Audio Media) {print_str} job has been created: ",
                json.dumps(result["Job"], indent=4, sort_keys=True),
            )
        return [mp3_create_job_result, mpd_create_job_result]
