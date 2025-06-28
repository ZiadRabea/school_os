from django.shortcuts import render, redirect
from .models import Teacher, Constant, Attendance
from .filters import TeacherFilter
from .forms import Absence, ProfilePic
from datetime import datetime, date
from django.db.models import Sum, Count
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from reports.models import TeacherReport
# Create your views here.

def access_denied(request):
    return render(request, "error.html")

@login_required
def home(request):
    if request.user.profile.type == "School":
        return redirect("/teachers")
    elif request.user.profile.type == "Teacher":
        return redirect("/students")
    elif request.user.profile.type == "Parent":
        return redirect("/students/mykids")
    else:
        return redirect("/accounts/login")

@login_required
def teachers(request):
    if request.user.profile.type == "School":
        teachers = Teacher.objects.filter(school=request.user.profile)
        filter = TeacherFilter(request.GET, queryset=teachers)
        teachers = filter.qs

        context = {
            "teachers" : teachers,
            "filter": filter
        }
        return render(request, "teachers.html", context)
    else :
        return redirect("/error")
# We can edit this so that teachers are not accessible except for the scools they work for.  | DONE 
@login_required
def profile(request, id):
    if request.user.profile.type == "School":
        teacher = Teacher.objects.get(id=id)
        if teacher.school == request.user.profile:
            if request.method == "POST":
                profilepicform = ProfilePic(request.POST, request.FILES, instance=teacher)
                if profilepicform.is_valid():
                    profilepicform.save()
                    return redirect(f"/teacher/{teacher.id}")
            else:
                profilepicform = ProfilePic(instance=teacher)
            context = {
                "teacher" : teacher,
                "form": profilepicform
            }
            return render(request, "profile.html", context)
        else:
            return redirect("/error")
    else:
        return redirect("/error")
    
@login_required
def register_absence(request):
    if request.user.profile.type == "School":
        if request.method == "POST":
            form = Absence(request.POST, request.FILES)
            if form.is_valid():
                myform = form.save(commit=False)
                # print(type(request.POST["deduction"]))
                # print(request.POST)
                hours = 8*22
                hourly_wage = myform.teacher.salary/hours
                if request.POST["deduction"] == "day":
                    myform.Salary_deduction = hourly_wage * 8
                elif request.POST["deduction"] == "half day":
                    myform.Salary_deduction = hourly_wage * 4
                else:
                    myform.Salary_deduction = 0
                myform.attendance = False
                myform.save()
                return redirect("/attendance")
        else:
            form = Absence()

        context = {
            "form": form
        }
        return render(request, "register_absence.html", context)
    else:
        return redirect("/error")

@login_required
def attendance(request):
    if request.user.profile.type == "School":
        school = request.user.profile
        try:
            attendances = Attendance.objects.filter(teacher__school=request.user.profile, time__date = date.today())
            time = school.time
        except:
            attendance = None
            time = None
        
        for attendance in attendances:
            if not attendance.attendance or attendance.Salary_deduction:
                pass
            else :
                created_time = datetime.combine(attendance.time.date(), attendance.time.time())
                time_difference = (created_time - datetime.combine(timezone.now().date(), time)).total_seconds() // 60
                attendance.difference = time_difference
                hours = 8*22
                hourly_wage = attendance.teacher.salary/hours
                dpm = hourly_wage/60
                attendance.Salary_deduction = time_difference*dpm
                attendance.save()
        context = {
            "attendances": attendances
        }
        return render(request, "attendance.html", context)
    else:
        return redirect("/error")
@login_required
def teacher_summary(request, id):
    if request.user.profile.type == "School":
        teacher = Teacher.objects.get(id = id)
        attendances = Attendance.objects.filter(teacher=teacher)
        late_minutes = attendances.aggregate(late_mins=Sum("difference"))["late_mins"] or 0
        total_absences = attendances.filter(attendance=False).count()
        total_salary_deduction = attendances.aggregate(total_deduction=Sum('Salary_deduction'))['total_deduction'] or 0
        total_salary = teacher.salary-total_salary_deduction
        context={
            "teacher": teacher,
            "late_minutes": late_minutes,
            "total_absences": total_absences,
            "total_salary_deduction": total_salary_deduction,
            "total_salary": total_salary
        }
        return render(request, "summary.html", context)
    else:
        return redirect("/error")

@login_required
def teacher_reports(request, id):    
        teacher = Teacher.objects.get(id = id)
        if request.user.profile.type == "School" or request.user.profile.teacher == teacher:
            reports = TeacherReport.objects.filter(teacher=teacher)
            context={
                "teacher": teacher,
                "reports": reports
            }
            return render(request, "treports.html", context)
        else:
            return redirect("/error")


@login_required   
def clearcache(request, id):
    teacher = Teacher.objects.get(id=id)
    if request.user.profile == teacher.school:
        attendance = Attendance.objects.filter(teacher=teacher)
        attendance.delete()
        return redirect(f"/teacher/{teacher.id}")
    else:
        return redirect("/error")


@login_required   
def clear_reports(request, id):
    teacher = Teacher.objects.get(id=id)
    if request.user.profile == teacher.school:
        reports = TeacherReport.objects.filter(teacher=teacher)
        reports.delete()
        return redirect(f"/teacher/{teacher.id}")
    else:
        return redirect("/error")
        