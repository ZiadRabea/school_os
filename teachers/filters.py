import django_filters
from .models import Teacher
class TeacherFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Teacher
        fields = ['name', 'subject', 'salary']