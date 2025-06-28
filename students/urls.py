from django.urls import path
from .views import *
urlpatterns = [
    path('', students),
    path('grades', grades),
    path('grades/<str:grade>', classes),
    path('grades/<str:grade>/<str:cls>', student_attendance),
    path('grades/<str:grade>/<str:cls>/confirm', confirm),
    path('grades/<str:grade>/<str:cls>/<int:id>/absence', sAbsence),
    path("reset_student_absence", reset),
    path('add', add_students),
    path('mykids', parent_portal),
    path('<int:id>', profile),
    path('<int:id>/remove', delete_student),
    path('<int:id>/edit', edit_student),
    path('<int:id>/clean_reports', clean_reports),
    ]
