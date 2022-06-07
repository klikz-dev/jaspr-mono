from django.contrib import admin
from jaspr.apps.stability_plan.models import (
    PatientWalkthrough,
    PatientWalkthroughStep,
    Step,
    Walkthrough,
    WalkthroughStep,
)


@admin.register(Walkthrough)
class WalkthroughAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "status",
    )
    list_filter = ("status",)
    search_fields = ("name",)


@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "content_type",
        "frontend_render_type",
        "object_id",
        "skip_if_blank",
        "function",
        "status",
    )
    list_filter = ("status", "frontend_render_type", "content_type", "skip_if_blank")
    search_fields = ("name",)


@admin.register(WalkthroughStep)
class WalkthroughStepAdmin(admin.ModelAdmin):
    list_display = (
        "step",
        "walkthrough",
        "order",
        "status",
    )
    list_editable = ("order",)
    list_filter = (
        "status",
        "walkthrough",
        "step",
    )
    search_fields = ("step__name",)
    raw_id_fields = ("step",)
    ordering = ("walkthrough", "order")


class PatientWalkthroughStepInline(admin.TabularInline):
    extra = 0
    model = PatientWalkthroughStep
    readonly_fields = ("id",)
    raw_id_fields = ("step",)


@admin.register(PatientWalkthrough)
class PatientWalkthroughAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "patient",
        "walkthrough",
        "status",
        "created",
    )
    list_filter = ("status", "walkthrough", "created")
    search_fields = ("patient__ssid",)
    raw_id_fields = ("patient",)
    date_hierarchy = "created"
    inlines = (PatientWalkthroughStepInline,)


@admin.register(PatientWalkthroughStep)
class PatientWalkthroughStepAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "patient_walkthrough",
        "step",
        "value",
        "frontend_render_type",
        "status",
    )
    list_filter = (
        "status",
        "patient_walkthrough__walkthrough",
        "frontend_render_type",
        "step",
    )
    search_fields = ("patient_walkthrough__patient__ssid", "step__name")
    raw_id_fields = (
        "patient_walkthrough",
        "step",
    )
