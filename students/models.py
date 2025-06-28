from django.db import models
from Accounts.models import Profile
# Create your models here.

class Student(models.Model):
    name = models.CharField(max_length=100)
    grades = (("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5"), ("6", "6"), ("7", "7"), ("8", "8"), ("9", "9"), ("10", "10"), ("11", "11"), ("12", "12"))
    grade = models.CharField(max_length=20, choices=grades)
    classes = (("A", "A"), ("B", "B"), ("C", "C"), ("D", "D"))
    cls = models.CharField(max_length=5, choices=classes)
    school = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    registered = models.BooleanField(default=False)
    parent_number = models.CharField(max_length=13)
    absence_count = models.IntegerField(null=True, blank=True)
    attendance_registered = models.BooleanField(default=True)
    evaluated = models.BooleanField(default=False)
    total_positive_reports = models.IntegerField(default=0, null=True, blank=True)
    total_negative_reports = models.IntegerField(default=0, null=True, blank=True)
    
    @property
    def computed_rating(self):
        total_reports = self.total_positive_reports + self.total_negative_reports
        if total_reports == 0:
            return 0  # No reports, no rating
        return round((self.total_positive_reports / total_reports) * 5, 1)

    def __str__(self):
        return self.name
