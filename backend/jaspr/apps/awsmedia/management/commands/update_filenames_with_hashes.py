import json
import os

import boto3
from django.conf import settings

from jaspr.apps.awsmedia.models import Media
from jaspr.apps.common.management.base import JasprBaseCommand
from jaspr.apps.common.storages import MediaRootS3Boto3Storage


class Command(JasprBaseCommand):
    """ Iterate through Media Records and Historical Media Records, adding hashes to filenames. """

    help = __doc__

    def handle(self, *args, **kwargs):
        client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )

        media_records = Media.objects.all()
        for media in media_records:
            # media = Media.objects.filter(file_type="graphic").get()
            original_name = media.file_field_original_name
            print(f"{original_name}")

            # instead of:
            # etag = MediaRootS3Boto3Storage.calculate_file_md5(media.file_field.file)
            # We'll get an etag that is often an md5 hash
            response = client.head_object(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=original_name
            )
            etag = json.loads(response["ResponseMetadata"]["HTTPHeaders"]["etag"])
            file_root, file_ext = os.path.splitext(media.file_field.name)
            new_name = f"{file_root}-{etag}{file_ext}"
            media.file_field.name = new_name

            copy_source = {
                "Bucket": settings.AWS_STORAGE_BUCKET_NAME,
                "Key": original_name,
            }
            client.copy_object(
                CopySource=copy_source,
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                Key=new_name,
            )

            client.delete_object(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                Key=original_name,
            )
            Media.objects.filter(pk=media.pk).update(file_field=media.file_field)
            print(f"    {media.file_field.name}")

            # Choosing at this time to not change historic records as it's a bit complicated with low gain for risk involved.
