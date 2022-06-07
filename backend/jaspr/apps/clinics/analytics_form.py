from django import forms
from jaspr.apps.clinics.models import HealthcareSystem
from datetime import datetime, date
from django.utils import timezone


class AnalyticsActionForm(forms.Form):
    analytic_choices = (
        ('visits', 'Visits'),
        ('actions', 'Actions'),
        ('ssi', 'SSI'),
        ('technicians', 'Technicians'),
        ('activities', 'Activities'),
        ('videos', 'Videos'),
        ('encounters', 'Encounters'),
    )
    system = forms.ModelChoiceField(queryset=HealthcareSystem.objects.all())
    analytics = forms.TypedChoiceField(choices=analytic_choices)
    start_date = forms.DateField(widget=forms.widgets.SelectDateWidget(years=range(2019, date.today().year + 1)))
    end_date = forms.DateField(widget=forms.widgets.SelectDateWidget(years=range(2019, date.today().year + 1)))

    include_mrn = forms.BooleanField(required=False, initial=False)
    include_analytics_token = forms.BooleanField(required=False, initial=True)
