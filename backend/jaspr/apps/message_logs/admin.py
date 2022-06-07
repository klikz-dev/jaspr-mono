from django.contrib import admin

from .models import EmailLog, SMSLog


class EmailLogAdmin(admin.ModelAdmin):
    list_display = (
        "user_id",
        "user_email",
        "date",
        "subject",
        "text_body",
        "html_body",
        "email_response",
    )
    search_fields = ("user_id", "user_email")
    list_filter = ("date",)
    ordering = ("-date", "user_email")


class SMSLogAdmin(admin.ModelAdmin):
    list_display = ("recipient_id", "title", "body", "sent", "status")
    search_fields = ("recipient_id", "title")
    list_filter = ("created",)
    ordering = ("-created", "recipient_id")


admin.site.register(EmailLog, EmailLogAdmin)
admin.site.register(SMSLog, SMSLogAdmin)
