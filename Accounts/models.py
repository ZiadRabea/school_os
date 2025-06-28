from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
#from teachers.models import Teacher
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    USERNAME_FIELD = None
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=13)
    types = (("School", "School"),("Teacher", "Teacher"),("Parent", "Parent"))
    # teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True)
    school = models.ForeignKey("Profile", on_delete=models.CASCADE, null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    type = models.CharField(max_length=10, choices=types)
    completed = models.BooleanField(default=False)
    def __str__(self):
        return str(self.user)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
