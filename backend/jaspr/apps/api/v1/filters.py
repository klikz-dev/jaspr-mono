from rest_framework import filters as rest_filters

# NOTE: We want to use this, but may need to upgrade DRF/Django-filter
# in order to have this working.
# class JasprMediaFilter(filters.FilterSet):
#     # `tags__name__iexact` is the correct lookup expression since
#     # we're using `taggit`'s `TaggableManager`.
#     # (Could also do a custom method and use `tags__name__in=[value]`)
#     # https://django-taggit.readthedocs.io/en/latest/api.html#filtering
#     tags = filters.CharFilter(lookup_expr='name__iexact')
#     # tags = filters.CharFilter(method='test_filter')

#     # def test_filter(self, queryset, name, value):
#     #     print("HELLLOOOOOO")
#     #     print(name)
#     #     print(value)
#     #     return queryset.filter(**{f'{name}__name__iexact': value})

#     class Meta:
#         model = JasprMedia
#         fields = ['tags']


# NOTE: We may want to use `JasprMediaFilter`, but may need DRF/django-filter
# upgrades in order to get things working properly.
class JasprMediaFilterBackend(rest_filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        tag = request.query_params.get("tag")
        if tag:
            return queryset.filter(tags__name__iexact=tag)
        return queryset


class PatientOwnerFilterBackend(rest_filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        # Return records for this patient user only.
        return queryset.filter(patient__user=request.user)


class JAHPatientOwnerFilterBackend(rest_filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        # Return records for this patient user only.
        return queryset.filter(jah_account__patient__user=request.user)


class DepartmentFilterBackend(rest_filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        # Return the cliniclocations for this technician user only.
        return queryset.filter(departmenttechnician__technician__user=request.user)
