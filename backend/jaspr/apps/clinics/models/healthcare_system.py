import logging
import operator
import pytz
from ipaddress import IPv4Address, IPv4Network, IPv6Address, IPv6Network
from typing import Any, Dict, Optional, Tuple, Union

from django.core.exceptions import ValidationError
from django.apps import apps
from django.db import models

from django_better_admin_arrayfield.models.fields import (
    ArrayField as BetterAdminArrayField,
)
from fernet_fields import EncryptedCharField
from model_utils import Choices
from netfields import CidrAddressField, InetAddressField
from simple_history.models import HistoricalRecords

from jaspr.apps.common.models import JasprAbstractBaseModel, RoutableModel

logger = logging.getLogger(__name__)


class PreferencesAbstractModel(JasprAbstractBaseModel):
    STATUS = Choices("active", "inactive", "archived")

    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))

    timezone = models.CharField(
        max_length=32,
        choices=TIMEZONES,
        null=True,
        blank=True,
        default="America/New_York"
    )
    provider_notes = models.BooleanField(
        null=True,
        blank=True,
        default=False,
        help_text="Allow providers to make comments on patient assessment answers"
    )
    narrative_note_template = models.ForeignKey(
        'kiosk.NoteTemplate',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="%(app_label)s_%(class)s_narrative_note_template",
    )
    stability_plan_template = models.ForeignKey(
        'kiosk.NoteTemplate',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="%(app_label)s_%(class)s_stability_plan_template",
    )
    consent_language = models.TextField(
        blank=True,
        null=True,
    )
    stability_plan_label = models.CharField(
        blank=False,
        null=False,
        default="Stability Plan",
        max_length=30,
        help_text="Customize the label for stability plans. Common options are \"Stability Plan\" or \"Safety Plan\""
    )

    class Meta:
        abstract = True


class GlobalPreferences(PreferencesAbstractModel):
    id = models.CharField(
        "id",
        primary_key=True,
        choices=Choices("global_preferences"),
        default="global_preferences",
        max_length=18
    )

    class Meta:
        verbose_name = "Global Preference"
        verbose_name_plural = "Global Preferences"

class Preferences(PreferencesAbstractModel):

    label = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="Enter a value in this field to help identify the purpose of this record."
    )

    class Meta:
        verbose_name = "Preferences"
        verbose_name_plural = "Preferences"


class HealthcareSystem(JasprAbstractBaseModel):
    """
    Renamed this model. Used to be called Clinic.
    """

    STATUS = Choices("active", "inactive", "archived")

    name = models.CharField("Name", max_length=125)

    activation_code = EncryptedCharField("Activation Code", blank=True, max_length=63)

    tablet_system_code = models.CharField(
        "Tablet System Code",
        max_length=32,
        blank=True,
        null=True,
        unique=True,
        help_text="Tablet system codes encoded in the URL must match "
                  "this code in order for the tablet to authenticate to this system"
    )

    organization_code = models.SlugField(
        help_text="Code used in subdomain of clinic portal.",
        unique=True,
    )

    preferences = models.ForeignKey(
        "clinics.Preferences",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    history = HistoricalRecords(bases=[RoutableModel])

    class Meta:
        verbose_name = "Healthcare System"
        verbose_name_plural = "Healthcare Systems"

    def __str__(self):
        return "%s" % (self.name)

    def save(self, *args, **kwargs):
        """All Clinics should have a clinic location 'unassigned'"""

        super().save(*args, **kwargs)

        # TODO: Can we only do this on create? Not the scope of the current ticket I'm
        # working on at the time of writing this comment, but seems like a create only
        # thing.
        Clinic.objects.get_or_create(
            system=self, name="unassigned", status="active"
        )

    def get_clinics_json(self):
        """Returns a JSON serializable list of locations"""
        locations = []
        for department in self.get_clinics():
            locations.append(
                {
                    "id": department.id,
                    "name": department.name,
                }
            )
        return locations

    def get_clinics(self):
        """Returns a list of Clinics for this HC System"""
        clinics = Clinic.objects.filter(system=self, status="active")
        return clinics

    def get_departments(self):
        result = []
        for clinic in self.get_clinics():
            for dept in clinic.get_departments():
                result.append(dept)
        return result

    def get_preferences(self):
        if self.preferences:
            return self.preferences
        try:
            global_preferences = GlobalPreferences.objects.get(pk="global_preferences")
            return global_preferences
        except GlobalPreferences.DoesNotExist:
            logger.warning("Global Preferences are not set")
        return None

    def has_technician(self, technician):
        """ Checks if a given technician belongs to system """
        return DepartmentTechnician.objects.filter(status="active",
                                                  department__clinic__system=self,
                                                  technician=technician).count() > 0


class Clinic(JasprAbstractBaseModel):
    """
    Renamed this model. Used to be called ClinicLocation
    """

    STATUS = Choices("active", "inactive", "archived")

    name = models.CharField("Name", max_length=125)
    system = models.ForeignKey(HealthcareSystem, on_delete=models.CASCADE, verbose_name="System")

    # IP Whitelisting
    ip_addresses_whitelist = BetterAdminArrayField(
        InetAddressField(verbose_name="IP Address"),
        blank=True,
        default=list,
        verbose_name="IP Addresses Whitelist",
        help_text=(
            "If you have individual IP Addresses (v4 or v6) to whitelist, you can add "
            "them here. At the time of writing, Jaspr only has IPv4 addresses though, "
            "so while you are welcome to add IPv6 addresses for the future, make sure to "
            "add at least one IPv4 address for the time being (if you are going to add an "
            "IP address in the first place)."
        ),
    )
    ip_address_ranges_whitelist = BetterAdminArrayField(
        CidrAddressField(verbose_name="IP Address Range (CIDR)"),
        blank=True,
        default=list,
        verbose_name="IP Address Ranges Whitelist (CIDR)",
        help_text=(
            "If you have IP (v4 or v6) address ranges as CIDR blocks, you can add "
            "them here. At the time of writing, Jaspr only has IPv4 addresses though, "
            "so while you are welcome to add IPv6 addresses for the future, make sure "
            "to add at least one IPv4 address range for the time being (if you are going "
            "to add an IP address range in the first place)."
        ),
    )

    preferences = models.ForeignKey(
        "clinics.Preferences",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    history = HistoricalRecords(bases=[RoutableModel])

    class Meta:
        verbose_name = "Clinic"
        verbose_name_plural = "Clinics"

    def __str__(self):
        return "{}: {}".format(self.system.name, self.name)

    def sort_and_uniqueify_whitelists(self) -> None:
        def address_sorting_func(
            value: Union[str, IPv4Address, IPv6Address]
        ) -> Tuple[int, Union[IPv4Address, IPv6Address]]:
            if isinstance(value, str):
                field = self._meta.get_field("ip_addresses_whitelist").base_field
                assert isinstance(
                    field, InetAddressField
                ), "If this changes, make sure to check/change/update this key function."
                ip_address_value = field.to_python(value)
            else:
                ip_address_value = value
            return (ip_address_value._version, ip_address_value)

        def address_range_sorting_func(
            value: Union[str, IPv4Network, IPv6Network]
        ) -> Tuple[int, Union[IPv4Network, IPv6Network]]:
            if isinstance(value, str):
                field = self._meta.get_field("ip_address_ranges_whitelist").base_field
                assert isinstance(
                    field, CidrAddressField
                ), "If this changes, make sure to check/change/update this key function."
                ip_network_value = field.to_python(value)
            else:
                ip_network_value = value
            return (ip_network_value._version, ip_network_value)

        # Make the IP Addresses and IP Address Ranges unique and sort them (the
        # underlying python types implement `__eq__` and other relevant comparison
        # operators). Did it this way partially because `__lt__` will throw a
        # `TypeError` if trying to compare IPv4 and IPv6 addresses/ranges.
        #
        # Also, this will transform any strings in the lists to their corresponding
        # underlying IP python values. Usually, in practice, `clean` has already done
        # that but this lets it be done also outside of `clean` (and made writing tests
        # easier when wanting to specify IP Addresses as strings).
        self.ip_addresses_whitelist = list(
            map(
                operator.itemgetter(1),
                sorted(map(address_sorting_func, set(self.ip_addresses_whitelist))),
            )
        )
        self.ip_address_ranges_whitelist = list(
            map(
                operator.itemgetter(1),
                sorted(
                    map(
                        address_range_sorting_func,
                        set(self.ip_address_ranges_whitelist),
                    )
                ),
            )
        )

    def save(self, *args, **kwargs):
        self.sort_and_uniqueify_whitelists()

        super().save(*args, **kwargs)

    @property
    def has_ip_whitelisting(self) -> bool:
        return bool(self.ip_addresses_whitelist) or bool(
            self.ip_address_ranges_whitelist
        )

    def ip_satisfies_whitelisting(self, ip_address: str) -> bool:
        if not self.has_ip_whitelisting:
            return True
        # NOTE: `ip_address` at this point is assumed to be a valid IPv4 or IPv6
        # string. Validation, if needed, should have been done before calling this
        # method.
        given_ip_address_value = InetAddressField().to_python(ip_address)
        for ip_address_value in self.ip_addresses_whitelist:
            if given_ip_address_value == ip_address_value:
                return True
        for ip_address_range in self.ip_address_ranges_whitelist:
            if given_ip_address_value in ip_address_range:
                return True
        return False

    def get_departments(self):
        return Department.objects.filter(clinic=self, status="active")

    def get_preferences(self):
        if self.preferences:
            return self.preferences
        return self.system.get_preferences()

    def has_technician(self, technician):
        """ Checks if a given technician belongs to clinic """
        return DepartmentTechnician.objects.filter(status="active", department__clinic=self,
                                                   technician=technician).count() > 0



class Department(JasprAbstractBaseModel):
    STATUS = Choices("active", "inactive", "archived")

    clinic = models.ForeignKey(Clinic, on_delete=models.PROTECT, db_constraint=False)
    name = models.CharField("Name", max_length=125)

    preferences = models.ForeignKey(
        "clinics.Preferences",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    tablet_department_code = models.CharField(
        "Tablet Department Code",
        max_length=32,
        blank=True,
        null=True,
        unique=True,
        help_text="Tablet department codes encoded in the URL must match "
                  "this code in order for the tablet to authenticate to this department"
    )

    @classmethod
    def get_by_system_and_name(clz, system, name):
        return Department.objects.filter(clinic__system=system, name=name).first()

    def get_department_ehr(self):
        """Returns the clinic EHR Object if it exists"""
        EpicDepartmentSettings = apps.get_model("epic.EpicDepartmentSettings")
        return EpicDepartmentSettings.for_department(self)

    def get_preferences(self):
        if self.preferences:
            return self.preferences
        return self.clinic.get_preferences()

    def has_technician(self, technician):
        """ Checks if a given technician belongs to department """
        return DepartmentTechnician.objects.filter(status="active", department=self, technician=technician).count() > 0

    def __str__(self):
        return f"({self.pk}) {self.name} ({self.clinic.system.name} / {self.clinic.name})"



class DepartmentTechnician(JasprAbstractBaseModel):
    STATUS = Choices("active", "inactive", "archived")

    technician = models.ForeignKey("kiosk.Technician", on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, db_constraint=False)

    history = HistoricalRecords(bases=[RoutableModel])

    class Meta:
        verbose_name = "Department Technician"
        verbose_name_plural = "Department Technician Records"
        unique_together = (("technician", "department"),)

    def __str__(self):
        return "%s - %s" % (self.department, self.technician)

    def clean(self):
        if self.technician.system != self.department.clinic.system:
            raise ValidationError(
                "Department has a Healthcare System that does not match the Healthcare System on Technician."
            )

    def save(self, *args, **kwargs):
        """ Keep technician in own clinic locations only. """

        self.full_clean()

        super().save(*args, **kwargs)
