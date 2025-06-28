from django.shortcuts import render, redirect
from.forms import *
from teachers.models import Teacher
from students.models import Student
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def create_student_report(request, id):
    student = Student.objects.get(id=id)

    if request.user.profile.type == "School" or request.user.profile.type == "Teacher":
        if request.method == "POST":
            form = SReportForm(request.POST, request.FILES)
            if form.is_valid():
                instance = form.save(commit = False)
                instance.student = student
                student.total_positive_reports += 1 if instance.is_positive else 0
                student.total_negative_reports += 1 if not instance.is_positive else 0
                instance.save()
                student.save()
                return redirect(f"/students/{instance.student.id}")
        else:
            form = SReportForm()
        
        context = {
            "form" : form
        }
        
        return render(request, "SReport.html", context)
    else:
        return redirect("/error")

@login_required
def create_teacher_report(request, id):
    teacher = Teacher.objects.get(id=id)
    if request.user.profile.type == "School":
        if request.method == "POST":
            form = TReportForm(request.POST, request.FILES)
            if form.is_valid():
                instance = form.save(commit = False)
                instance.teacher = teacher
                teacher.total_positive_reports += 1 if instance.is_positive else 0
                teacher.total_negative_reports += 1 if not instance.is_positive else 0
                instance.save()
                teacher.save()
                return redirect(f"/teacher/{teacher.id}/reports")
        else:
            form = TReportForm()
        
        context = {
            "form" : form
        }
        
        return render(request, "TReport.html", context)
    else:
        return redirect("/error")
