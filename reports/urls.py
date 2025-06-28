from django.urls import path
from .views import *
urlpatterns = [
    path('students/<int:id>/add', create_student_report),
    path('teachers/<int:id>/add', create_teacher_report),
    ]
