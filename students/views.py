from django.shortcuts import render, redirect
from .models import *
from .forms import *
from .filters import *
from reports.models import *
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def add_students(request):
    if request.user.profile.type == 'School':
        if request.method == "POST":
            form = StudentForm(request.POST, request.FILES)
            if form.is_valid():
                student = form.save(commit=False)
                student.school = request.user.profile
                student.attendance_registered = True
                student.save()
                return redirect("/students")
        else:
            form = StudentForm()

        context = {
            "form": form
        }

        return render(request, "add_student.html", context)
    else:
        return redirect("/error")

@login_required
def students(request):
    user = request.user.profile
    if user.type == "School":
            students = Student.objects.filter(school=user)
    elif user.type == "Teacher":
            students = Student.objects.filter(school=user.school)
    else:
        return redirect("/error")
    filter = StudentFilter(request.GET, queryset=students)
    students = filter.qs
    context = {
        "students": students,
        "filter" : filter
    }
    return render(request, "students_list.html", context)

    
def profile(request, id):
    student = Student.objects.get(id=id)
    reports = StudentReport.objects.filter(student=student, is_sent=False)

    context = {
        "student" : student,
        "reports" : reports 
    }

    return render(request, "student_profile.html", context)

@login_required
def clean_reports(request, id):
    if request.user.profile.type == "School":
        student = Student.objects.get(id=id)
        StudentReport.objects.filter(student=student).delete()
        return redirect(f"/students/{id}") 
    else:
        return redirect("/error")

@login_required
def delete_student(request, id):
    if request.user.profile.type == "School":
        student = Student.objects.get(id=id)
        student.delete()
        return redirect("/students")
    else:
        return redirect("/error")
    
@login_required
def edit_student(request, id):
    if request.user.profile.type == "School":
        student = Student.objects.get(id=id)
        if request.method == "POST":
            form = StudentForm(request.POST, request.FILES, instance=student)
            if form.is_valid():
                myform = form.save(commit=False)
                myform.school = request.user.profile
                myform.save()
                return redirect("/students")
        else:
            form = StudentForm(instance=student)

        context = {
            "form": form
        }
        return render(request, "add_student.html", context)
    else:
        return redirect("/error")

def parent_portal(request):
    students = Student.objects.filter(parent_number = request.user.profile.phone)

    context = {
        "students": students
    }

    return render(request, "parent.html", context)

def grades(request):
    if request.user.profile.type == "School" or request.user.profile.type == "Teacher":
        return render(request, "grades.html")
    else:
        return redirect("/error")
def classes(request, grade):
    if 0 >= int(grade) or int(grade) > 12: return redirect("/error")
    if request.user.profile.type == "School" or request.user.profile.type == "Teacher":
        context = {
            "grade": grade
        }
        return render(request, "classes.html", context)
    else:
        return redirect("/error")

def student_attendance(request, grade, cls):
    if not cls in "ABCD": return redirect("/error")
    if 0 >= int(grade) or int(grade) > 12: return redirect("/error")
    #school = request.user.profile if request.user.profile.type == "School" else request.user.profile.school
    if request.user.profile.type == "School" or request.user.profile.type == "Teacher":
        students = Student.objects.filter(grade=grade, cls=cls, school=request.user.profile if request.user.profile.type=="School" else request.user.profile.school)

        context = {
            "students": students,
            "grade": grade,
            "class": cls
        }

        return render(request, "student_attendance.html", context)
    else:
        return redirect("/error")
    
def sAbsence(request, grade, cls, id):
    if request.user.profile.type in ["School", "Teacher"]:
        student = Student.objects.get(id=id)
        school = request.user.profile if request.user.profile.type == "School" else request.user.profile.school

        if student.grade == grade and student.cls == cls and student.school == school:
            student.attendance_registered = False
            student.evaluated = True
            student.absence_count += 1
            student.save()
            return redirect(f"/students/grades/{grade}/{cls}")
        else:
            return redirect("/error")
    else:
        return redirect("/error")

def confirm(request, grade, cls):
    if request.user.profile.type in ["School", "Teacher"]:
        school = request.user.profile if request.user.profile.type == "School" else request.user.profile.school

        Student.objects.filter(school=school, grade=grade, cls=cls).update(evaluated=True)
        return redirect(f"/students/grades/{grade}/{cls}")
    else:
        return redirect("/error")

def reset(request):
    if request.user.profile.type == "School":
        Student.objects.filter(school=request.user.profile).update(evaluated=False, attendance_registered=True)
        return redirect("/")
    else:
        return redirect("/error")