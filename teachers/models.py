from django.db import models
from Accounts.models import Profile
from cloudinary_storage.storage import MediaCloudinaryStorage
# Create your models here.
class Teacher(models.Model):
    name = models.CharField(max_length = 100)
    school = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="t_school")
    teacher = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="teacher", null=True, blank=True)
    subjects = (("Arabic", "Arabic"), ("English", "English"), ("French", "French"), ("Math", "Math"), ("Physics", "Physics"))
    subject = models.CharField(max_length=50, choices=subjects)
    email = models.EmailField()
    pic = models.ImageField(null=True, blank=True, upload_to="profilepics", storage=MediaCloudinaryStorage)
    image = models.CharField(max_length=1000)
    phone = models.CharField(max_length=13)
    salary = models.IntegerField()
    rating = models.IntegerField()
    total_positive_reports = models.IntegerField(default=0, null=True, blank=True)
    total_negative_reports = models.IntegerField(default=0, null=True, blank=True)
    
    @property
    def computed_rating(self):
        total_reports = self.total_positive_reports + self.total_negative_reports
        if total_reports == 0:
            return 0  # No reports, no rating
        return round((self.total_positive_reports / total_reports) * 5, 1)

    def __str__(self):
        return str(self.name)

class Attendance(models.Model):
    attendance = models.BooleanField(default=True)
    time = models.DateTimeField(auto_now_add=True)
    difference = models.IntegerField(null = True, blank=True)
    permission = models.BooleanField(default=False)
    Salary_deduction = models.IntegerField(blank=True, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.teacher.name)
    
class Constant(models.Model):
    school = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    value = models.IntegerField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} | {self.value if self.value else "None"} | {self.time}"
