import datetime

from django.db.models import DateTimeField, OuterRef, Prefetch, Subquery

from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.request import Request
from rest_framework.generics import get_object_or_404

from .jaspr_base import JasprBaseViewSetMixin
from jaspr.apps.api.v1.permissions import (
    IsInER,
    IsTechnician,
    SatisfiesClinicIPWhitelistingFromTechnician,
    SharesClinic,
)
from jaspr.apps.api.v1.serializers import (
    PatientSerializer,
    ReadOnlyTechnicianPatientSerializer
)
from jaspr.apps.kiosk.models import (
    Patient,
    ActivateRecord,
    Encounter,
    PatientDepartmentSharing,
)
from jaspr.apps.api.v1.permissions import HasRecentHeartbeat, IsAuthenticated

from fuzzywuzzy import fuzz

from ..exceptions import AlreadyExistsError
from ..serializers import ActivateNewPatientSerializer

PATIENT_SEARCH_PROPERTIES = ("mrn", "ssid", "first_name", "last_name")


class TechnicianPatientViewSet(
    JasprBaseViewSetMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):
    """

    /v1/technician/patients/1/

    GET

        {
            "id": 1,
            "encounter": 1,
            "firstName": "John",
            "lastName": "Smith",
            "dateOfBirth": "1970-02-17"
            "mrn": "23412lkjh12l3jl12kh3",
            "clinicLocation": 1,
            "mobilePhone": "5555555555",
            "email": "john.smith@example.com"
        },

        or

        {
            "id": 1,
            "encounter": 1,
            "ssid" "123424-234hljksdlfkj_23423lsdfj_234234d",
            "clinicLocation": 1,
            "mobilePhone": "5555555555",
            "email": "john.smith@example.com"
        }

    PUT
        {
            "firstName": "John",
            "lastName": "Smith",
            "dateOfBirth": "1970-02-17"
            "mrn": "23412lkjh12l3jl12kh3",
            "clinicLocation": 1,
            "mobilePhone": "5555555555",
            "email": "john.smith@example.com"
        },

        or

        {
            "ssid" "123424-234hljksdlfkj_23423lsdfj_234234d",
            "clinicLocation": 1,
            "mobilePhone": "5555555555",
            "email": "john.smith@example.com"
        }

    """

    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = (
        IsAuthenticated,
        IsTechnician,
        IsInER,
        SharesClinic,
        SatisfiesClinicIPWhitelistingFromTechnician,
    )

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed("PATCH")

    @action(methods=["get"], detail=True)
    def note(self, request, pk=None):
        """Custom route to return a note to a technician for a patient

        GET /v1/technician/patients/1/note

            {“body”: “NARRATIVE NOTE GOES HERE”}

        """

        patient = self.get_object()
        encounter = patient.current_encounter
        if encounter:
            data = encounter.narrative_note
        else:
            # TODO / Note, right now, it's possible for patients not to have a current encounter.
            # Once we have encounter switching in the UX, we can remove this else statement as we
            # should always be able to find a relevant encounter
            data = {
                "narrative_note": "Patient has not begun Suicide Status Interview, no note available.",
                "stability_plan_note": "Patient has not begun a Crisis Stability Plan, no note available."
            }
        return Response(data=data, status=status.HTTP_200_OK)

    def create(self, request: Request):
        serializer = ActivateNewPatientSerializer(
            data=request.data, context={"request": request, "create_encounter": True}
        )
        try:
            serializer.is_valid(raise_exception=True)
        except AlreadyExistsError as e:
            existing_patient = get_object_or_404(
                TechnicianPatientViewSet.base_query(request.user.technician),
                pk=e.object_id,
            )
            serialized_existing_patient = ReadOnlyTechnicianPatientSerializer(
                instance=existing_patient, context={"request": request}
            ).data

            error_dict = {
                "message": str(e),
                "object": serialized_existing_patient,
            }
            return Response(error_dict, status=status.HTTP_409_CONFLICT)

        patient = serializer.save()
        patient_serializer = ReadOnlyTechnicianPatientSerializer(patient, context={"request": self.request})
        return Response(data=patient_serializer.data, status=status.HTTP_200_OK)

    def get_serializer_context(self):
        return {"request": self.request}

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def list(self, request: Request):
        technician = request.user.technician
        query = None
        if "q" in request.GET:
            query = request.GET["q"].strip().casefold()

        # If no query, return the technicians recent patients
        if query is None or query == "":
            return self.get_recent_patients(technician)

        # Check if query is a date of birth (dob)
        # Return patients with matching dob
        try:
            dob = datetime.datetime.strptime(query, "%m/%d/%Y").date()
            return self.get_patients_by_dob(technician, dob)
        except ValueError as e:
            pass

        # Check if query is a dob without a year AND add the year for the last occurrence of that date.
        # Return patients with matching dob
        try:
            dob = datetime.datetime.strptime(query, "%m/%d").date()
            return self.get_patients_by_month_and_day(technician, dob.month, dob.day)
        except ValueError as e:
            pass

        # The query must be either a MRN or SSID or first name or last name
        return self.search(technician, query)

    @staticmethod
    def base_query(technician):
        # get the department ids for the technician
        department_ids = technician.departmenttechnician_set.filter(
            status="active"
        ).values_list("department", flat=True)

        activate_record_subquery = (
            ActivateRecord.objects.filter(
                patient_id=OuterRef("pk"),
                # NOTE: This currently partially assumes to some extent that the
                # `Technician`'s `clinic` doesn't change after being initially set. If
                # `clinic` is added to `ActivateRecord` (and/or `department`),
                # then we can refactor this and use that instead.
                technician__system=technician.system,
            )
                .order_by("-timestamp")
                .values("timestamp")[:1]
        )

        patient_query = Patient.objects.select_related('user') \
            .prefetch_related(
            Prefetch("patientdepartmentsharing_set",
                     queryset=PatientDepartmentSharing.objects.filter(status="active"))) \
            .filter(patientdepartmentsharing__department__in=department_ids) \
            .distinct()

        query = Patient.get_related_query(patient_query).annotate(
            last_logged_in_at=Subquery(
                activate_record_subquery, output_field=DateTimeField(null=True)
            )
        ).order_by("-last_logged_in_at")

        return query

    def get_patients_by_dob(self, technician, dob):
        results = []
        for patient in self.base_query(technician):
            if patient.date_of_birth == dob:
                results.append(patient)
            # We only want to return a max of 30
            if len(results) >= 30:
                break
        serializer = ReadOnlyTechnicianPatientSerializer(results, context={"request": self.request}, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def get_patients_by_month_and_day(self, technician, month, day):
        results = []
        for patient in self.base_query(technician):
            if (
                    patient.date_of_birth is not None
                    and patient.date_of_birth.month == month
                    and patient.date_of_birth.day == day
            ):
                results.append(patient)
            # We only want to return a max of 30
            if len(results) >= 30:
                break
        serializer = ReadOnlyTechnicianPatientSerializer(results, context={"request": self.request}, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def search(self, technician, query):
        results = []
        for patient in self.base_query(technician):
            for prop in PATIENT_SEARCH_PROPERTIES:
                patient_value = getattr(patient, prop)
                if patient_value is not None:
                    patient_value = patient_value.casefold()
                fuzz_value = fuzz.partial_ratio(patient_value, query)
                if fuzz_value >= 90:
                    results.append(patient)
                    break
            # We only want to return a max of 30
            if len(results) >= 30:
                break

        serializer = ReadOnlyTechnicianPatientSerializer(results, context={"request": self.request}, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def get_recent_patients(self, technician):

        query = self.base_query(technician)

        # NOTE (EBPI-936): Return at most `30` recent `Patient`s right now.
        # With upcoming search work, current spec is to not paginate, but
        # rather just return this relatively high number and let the technician
        # search for more specific information if the last `30` isn't enough
        # without a search.
        queryset = query[:30]
        serializer = ReadOnlyTechnicianPatientSerializer(queryset, context={"request": self.request}, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

