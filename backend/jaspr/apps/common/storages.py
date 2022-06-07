import hashlib
import os

from django.core.files import File
from storages.backends.s3boto3 import S3Boto3Storage


class MediaRootS3Boto3Storage(S3Boto3Storage):
    # NOTE: We use to the root of the S3 bucket for storing the media files right now.
    # * NOTE/TODO: Is this what we want?
    location = ""
    file_overwrite = False

    @staticmethod
    def calculate_file_md5(file_):

        if not file_:
            return ""
        md5 = hashlib.md5()
        for chunk in file_.chunks():
            md5.update(chunk)
        return md5.hexdigest()

    def save(self, name, content, max_length=None):
        """
        Overriding to enforce md5 appending.
        """
        # Get the proper name for the file, as it will actually be saved.
        if name is None:
            name = content.name

        if not hasattr(content, "chunks"):
            content = File(content, name)

        md5_hex = self.calculate_file_md5(content)
        file_root, file_ext = os.path.splitext(name)
        name = f"{file_root}-{md5_hex}{file_ext}"

        name = self.get_available_name(name, max_length=max_length)
        return self._save(name, content)
