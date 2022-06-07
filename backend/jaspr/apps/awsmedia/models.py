from django.conf import settings
from django.db import models
from django.utils.safestring import mark_safe
from model_utils import Choices
from simple_history.models import HistoricalRecords
from taggit.managers import TaggableManager

from jaspr.apps.awsmedia.fields import PrimaryFileField
from jaspr.apps.common.models import JasprAbstractBaseModel, RoutableModel


class BaseMedia(JasprAbstractBaseModel):
    """
    Attributes:
        file_field: django model field to store file
        file_type: stores type of file
        name: file name
        description: file description
        status: active or inactive
    """

    FILE_TYPE_CHOICES = (
        ("worksheet", "worksheet"),
        ("video", "video"),
        ("audio", "audio"),
        ("graphic", "graphic"),
        ("exercise", "exercise"),
        ("discussion points", "discussion points"),
    )
    TRANSCODE_STATUS_CHOICES = (
        ("new", "new"),  # newly uploaded
        ("queued", "queued"),  # sent to aws transcoder
        ("completed", "completed"),  # returned, transcoding complete
        ("non-video", "non-video"),  # for non-video media
    )

    STATUS = Choices("active", "inactive")

    # NOTE on fields, see commit hash: a3c27a5adb43cb9352e13ee8300b3659bd8494a9
    # (The extra fields that were added came from EBPI-89 issue/ticket regarding
    #  standardizing media by merging in iKinnect code/logic).
    name = models.CharField(max_length=256, unique=True)
    description = models.TextField(blank=True)
    file_field = models.FileField(max_length=510)
    subtitle_file = models.FileField(max_length=510, null=True, blank=True)
    transcript = models.TextField(blank=True)
    poster = models.FileField(max_length=510, null=True, blank=True)
    # NOTE: `fmp4_transcode` and `dash_playlist` are currently the same
    # thing/pointing to the same thing. TODO: Clean this up. We will need
    # (probably) a frontend release in order to do this.
    fpm4_transcode = models.FileField(max_length=510, null=True, blank=True)
    mp4_transcode = models.FileField(max_length=510, null=True, blank=True)
    mp3_transcode = models.FileField(max_length=510, null=True, blank=True)
    tips = models.TextField(blank=True, default="")
    # NOTE: `completion_time` is not currently used in the code unless set
    # by the admin in Jaspr. `duration` is in a similar situation, although
    # it was previously only defined on iKinnect.
    completion_time = models.IntegerField(null=True, blank=True)
    hls_playlist = models.FileField(max_length=510, null=True, blank=True)
    dash_playlist = models.FileField(max_length=510, null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)
    file_type = models.CharField(max_length=25, choices=FILE_TYPE_CHOICES)
    transcode_status = models.CharField(
        max_length=25, choices=TRANSCODE_STATUS_CHOICES, default="new"
    )
    order = models.PositiveSmallIntegerField(default=0)
    tags = TaggableManager(blank=True)

    history = HistoricalRecords(bases=[RoutableModel], inherit=True)

    def __str__(self):
        return f"{self.file_type} - {self.name} - {self.description}"

    class Meta:
        abstract = True


class Media(BaseMedia):
    @property
    def bucket(self):
        return settings.AWS_STORAGE_BUCKET_NAME

    @property
    def pipeline_id(self):
        return settings.AWS_TRANSCODE_PIPELINE_ID

    @property
    def file_prefix(self):
        return "kiosk"

    file_field = PrimaryFileField(max_length=510, verbose_name="File Field")
    file_field_original_name = models.CharField(
        max_length=510,
        verbose_name="Original Name of File",
        help_text="Original name of file_field before hashing.",
    )
    subtitle_file = models.FileField(
        max_length=510,
        null=True,
        blank=True,
        verbose_name="Subtitle File",
    )
    poster = models.ImageField(
        max_length=510,
        null=True,
        blank=True,
        verbose_name="Poster",
    )
    thumbnail = models.ImageField(
        max_length=510,
        null=True,
        blank=True,
        verbose_name="Thumbnail",
    )
    fpm4_transcode = models.FileField(
        max_length=510,
        null=True,
        blank=True,
        verbose_name="FMP4 Transcode",
    )
    mp4_transcode = models.FileField(
        max_length=510,
        null=True,
        blank=True,
        verbose_name="MP4 Transcode",
    )
    mp3_transcode = models.FileField(
        max_length=510,
        null=True,
        blank=True,
        verbose_name="MP3 Transcode",
    )
    hls_playlist = models.FileField(
        max_length=510,
        null=True,
        blank=True,
        verbose_name="HLS Playlist",
    )
    dash_playlist = models.FileField(
        max_length=510,
        null=True,
        blank=True,
        verbose_name="Dash Playlist",
    )

    class Meta:
        verbose_name = "Media"
        verbose_name_plural = "Media"

    def __str__(self):
        return self.file_field.name


class PrivacyScreenImage(JasprAbstractBaseModel):
    """ Container for photos used in Privacy Screen on Jaspr """

    STATUS = Choices(("active", "Active"), ("archived", "Archived"))

    @property
    def bucket(self):
        return settings.AWS_STORAGE_BUCKET_NAME

    image = models.ImageField(max_length=510)

    def admin_thumbnail(self):
        if self.image:
            return mark_safe(
                '<img src="%s" class="admin-thumbnail" />' % (self.image.url)
            )
        else:
            return "No Image"

    def __str__(self):
        if self.image:
            return f"{self.id} - {self.image.url}"
        else:
            return f"{self.id} - No url available"

    class Meta:
        verbose_name = "Privacy Screen Image"
        verbose_name_plural = "Privacy Screen Images"
