from django.urls import path
from .views import *
urlpatterns = [
    path('', home),
    path('teachers', teachers),
    path('error', access_denied),
    path('attendance', attendance),
    path('absence', register_absence),
    path('teacher/<int:id>', profile),
    path('teacher/<int:id>/reports', teacher_reports),
    path('teacher/<int:id>/clearcache', clearcache),
    path('teacher/<int:id>/reports/clear', clear_reports),
    path('teacher/<int:id>/summary', teacher_summary),
    ]
