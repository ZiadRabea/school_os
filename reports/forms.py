from django import forms
from .models import *


class TReportForm(forms.ModelForm):
    class Meta:
        model = TeacherReport
        fields = "__all__"

class SReportForm(forms.ModelForm):
    class Meta:
        model = StudentReport
        fields = "__all__"
