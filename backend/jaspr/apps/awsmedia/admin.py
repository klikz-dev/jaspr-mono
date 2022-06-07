from django.contrib import admin
from jaspr.apps.awsmedia.models import Media, PrivacyScreenImage
from simple_history.admin import SimpleHistoryAdmin


class MediaAdmin(SimpleHistoryAdmin):
    list_display = (
        "name",
        "file_type",
        "description",
        "transcode_status",
        "status",
        "created",
        "modified",
    )
    list_filter = ("file_type", "transcode_status", "status", "created", "modified")
    search_fields = ("name", "description")
    ordering = ("name", "created")
    actions = [
        "set_transcode_status_new",
        "set_transcode_status_queued",
        "set_transcode_status_complete",
    ]

    def set_transcode_status_new(self, request, queryset):
        queryset.update(transcode_status="new")

    set_transcode_status_new.short_description = "Set transcode status to 'new'."

    def set_transcode_status_queued(self, request, queryset):
        queryset.update(transcode_status="queued")

    set_transcode_status_queued.short_description = "Set transcode status to 'queued'."

    def set_transcode_status_complete(self, request, queryset):
        queryset.update(transcode_status="completed")

    set_transcode_status_complete.short_description = (
        "Set transcode status to 'completed'."
    )


class PrivacyScreenImageAdmin(SimpleHistoryAdmin):
    list_display = ("id", "admin_thumbnail", "status")
    list_filter = ("status",)

    class Media:
        css = {"all": ("common/css/admin_thumbnail.css",)}


admin.site.register(Media, MediaAdmin)
admin.site.register(PrivacyScreenImage, PrivacyScreenImageAdmin)
