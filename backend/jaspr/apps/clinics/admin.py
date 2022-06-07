import csv
import datetime
from django.utils import timezone

from django.conf.urls import url
from django.contrib import admin
from django.contrib.admin import StackedInline
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404, reverse
from django.utils.html import format_html
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin
from simple_history.admin import SimpleHistoryAdmin

from jaspr.apps.clinics.models import GlobalPreferences, Preferences, HealthcareSystem, Clinic, Department, \
    DepartmentTechnician
from jaspr.apps.kiosk.analytics import AnalyticsExporter
from .analytics_form import AnalyticsActionForm


class ClinicInline(StackedInline, DynamicArrayMixin):
    model = Clinic

    def get_extra(self, request, obj=None, **kwargs):
        if obj is None:
            return 1
        return 0


class DepartmentInline(StackedInline, DynamicArrayMixin):
    model = Department

    def get_extra(self, request, obj=None, **kwargs):
        if obj is None:
            return 1
        return 0


class GlobalPreferencesAdmin(SimpleHistoryAdmin, DynamicArrayMixin):
    list_display = (
        "timezone",
        "provider_notes"
    )


class PreferencesAdmin(SimpleHistoryAdmin, DynamicArrayMixin):
    list_display = (
        "label",
        "timezone",
        "provider_notes"
    )


class HealthcareSystemAdmin(SimpleHistoryAdmin):
    list_display = (
        "id",
        "name",
        "status",
        "organization_code",
        "jaspr_analytics",
    )
    search_fields = ("name", "organization_code")
    list_filter = (
        "status",
    )
    ordering = ("name",)
    inlines = [ClinicInline]

    def get_urls(self):
        return super().get_urls() + [
            url(
                r"^export-kiosk-analytics/(?P<system_id>[0-9]+)/(?P<data_name>.+)$",
                self.admin_site.admin_view(self.show_analytics_options),
                name="export-kiosk-analytics",
            )
        ]

    def show_analytics_options(self, request, system_id, data_name, *args, **kwargs):
        context = self.admin_site.each_context(request)
        if request.method != 'POST':
            system = HealthcareSystem.objects.get(pk=system_id)
            form = AnalyticsActionForm(initial={
                'system': system_id,
                'analytics': data_name,
                'start_date': system.created,
                'end_date': timezone.now()
            })

        else:
            form = AnalyticsActionForm(request.POST)
            if form.is_valid():
                system_id = request.POST['system']
                data_name = request.POST['analytics']
                start_date = datetime.date(
                    int(request.POST['start_date_year']),
                    int(request.POST['start_date_month']),
                    int(request.POST['start_date_day']),
                )
                end_date = datetime.date(
                    int(request.POST['end_date_year']),
                    int(request.POST['end_date_month']),
                    int(request.POST['end_date_day']),
                )
                include_mrn = request.POST.get('include_mrn', False) == 'on'
                include_analytics_token = request.POST.get('include_analytics_token', False) == 'on'
                return self.export_jaspr_analytics(system_id, data_name, start_date, end_date,
                                                   include_mrn=include_mrn,
                                                   include_analytics_token=include_analytics_token)

        context['form'] = form
        context['opts'] = self.model._meta
        context['title'] = "Export Analytics"
        context['show_close'] = True
        return TemplateResponse(
            request,
            'admin_analytics.html',
            context,
        )

    def jaspr_analytics(self, obj):
        # Thanks to https://medium.com/@hakibenita/how-to-add-custom-action-buttons-to-django-admin-8d266f5b0d41
        return format_html(
            '<a class="button" href="{}">Visits</a>&nbsp;'
            '<a class="button" href="{}">Actions</a>&nbsp;'
            '<a class="button" href="{}">SSI</a>&nbsp;'
            '<a class="button" href="{}">Activities</a>&nbsp;'
            '<a class="button" href="{}">Technicians</a>&nbsp;'
            '<a class="button" href="{}">Videos</a>&nbsp;'
            '<a class="button" href="{}">Encounters</a>',
            reverse("admin:export-kiosk-analytics", args=[obj.pk, "visits"]),
            reverse("admin:export-kiosk-analytics", args=[obj.pk, "actions"]),
            reverse("admin:export-kiosk-analytics", args=[obj.pk, "ssi"]),
            reverse("admin:export-kiosk-analytics", args=[obj.pk, "activities"]),
            reverse("admin:export-kiosk-analytics", args=[obj.pk, "technicians"]),
            reverse("admin:export-kiosk-analytics", args=[obj.pk, "videos"]),
            reverse("admin:export-kiosk-analytics", args=[obj.pk, "encounters"]),
        )

    jaspr_analytics.short_description = "Jaspr Analytics"
    jaspr_analytics.allow_tags = True

    def export_jaspr_analytics(self, system_id, data_name, start_date, end_date,
                               include_mrn=False,
                               include_analytics_token=True):
        system = get_object_or_404(HealthcareSystem, pk=system_id)
        exporter = AnalyticsExporter(system, start_date, end_date, include_mrn=include_mrn,
                                     include_analytics_token=include_analytics_token)
        if data_name == "visits":
            iterator = exporter.visit_log_iterator
        elif data_name == "actions":
            iterator = exporter.action_log_iterator
        elif data_name == "ssi":
            iterator = exporter.assessment_iterator
        elif data_name == "activities":
            iterator = exporter.skills_iterator
        elif data_name == "technicians":
            iterator = exporter.technicians_iterator
        elif data_name == "videos":
            iterator = exporter.videos_iterator
        elif data_name == "encounters":
            iterator = exporter.encounters_iterator
        else:
            raise Http404(f"Invalid data name: {data_name}")
        # NOTE: If the files ever get big enough to need streaming,
        # we could do something like this:
        # https://docs.djangoproject.com/en/1.11/howto/outputting-csv/#streaming-large-csv-files
        response = HttpResponse(content_type="text/csv")
        response[
            "Content-Disposition"
        ] = f'attachment; filename="system_{system.id}_jaspr_{data_name}_{start_date}--{end_date}.csv"'
        writer = csv.writer(response)
        for row in iterator:
            writer.writerow(row)
        return response


class ClinicAdmin(SimpleHistoryAdmin, DynamicArrayMixin):
    list_display = ("id", "name", "system", "status")
    search_fields = ("name",)
    list_filter = ("system", "status")
    ordering = ("system", "name")

    raw_id_fields = ("system",)

    inlines = [DepartmentInline]


class DepartmentAdmin(SimpleHistoryAdmin):
    list_display = ("id", "name", "clinic", "status")
    search_fields = ("name",)
    list_filter = ("clinic", "status")
    ordering = ("clinic", "name")

    raw_id_fields = ("clinic",)


class DepartmentTechnicianAdmin(SimpleHistoryAdmin):
    list_display = ("id", "department", "technician", "status")
    search_fields = ("department__name", "technician__user__email")
    list_filter = ("status",)
    ordering = ("department", "technician")

    raw_id_fields = ("department", "technician")


admin.site.register(GlobalPreferences, GlobalPreferencesAdmin)
admin.site.register(Preferences, PreferencesAdmin)
admin.site.register(HealthcareSystem, HealthcareSystemAdmin)
admin.site.register(Clinic, ClinicAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(DepartmentTechnician, DepartmentTechnicianAdmin)
