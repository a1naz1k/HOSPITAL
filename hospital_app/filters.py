from django_filters import FilterSet
from .models import Department, Specialty, Doctor


class DepartmentFilter(FilterSet):
    class Meta:
        model = Department
        fields = {
            'department_name': ['exact'],
            'level': ['gt', 'lt'],
        }


class SpecialtyFilter(FilterSet):
    class Meta:
        model = Specialty
        fields = {
            'specialty_name': ['exact'],
        }


class DoctorFilter(FilterSet):
    class Meta:
        model = Doctor
        fields = {
            'work_day': ['exact'],
            'service_price': ['gt', 'lt'],
        }
