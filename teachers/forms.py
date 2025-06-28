from django import forms
from .models import *
class Absence(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ["teacher", "permission"]
        
class ProfilePic(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ["pic"]
