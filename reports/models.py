from django.db import models
from students.models import Student
from teachers.models import Teacher
# Create your models here.

class StudentReport(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField(max_length=1000)
    is_positive = models.BooleanField(default=False, null=True, blank=True)
    is_sent = models.BooleanField(default=False, null=True, blank=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.student.name} : {self.title}"
    
class TeacherReport(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField(max_length=1000)
    is_positive = models.BooleanField(default=False, null=True, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f"{self.teacher.name} : {self.title}"