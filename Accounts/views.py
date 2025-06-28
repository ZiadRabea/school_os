from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import *
from django.contrib.auth.decorators import login_required
# Create your views here.

from django.shortcuts import render, redirect
from .forms import SignUP, ProfileInfo
from teachers.models import Teacher
from django.contrib.auth import authenticate, login

@login_required
def sign_up(request, id=None):
    if request.user.profile.type == "School":
        if request.method == 'POST':
            Form = SignUP(request.POST)
            if Form.is_valid():
                instance = Form.save()
                phone = request.POST["phone"]
                type = request.POST["type"]
                name = request.POST["full_name"]
                instance.profile.name = name
                instance.profile.type = type
                instance.profile.phone = phone
                if type == "Teacher" and id:
                    instance.profile.school = request.user.profile
                    instance.save()
                    teacher = instance.profile
                    teacher_instance = Teacher.objects.get(id=id)
                    teacher_instance.teacher = instance.profile
                    teacher_instance.save()
                instance.profile.save()
                username = Form.cleaned_data['username']
                password = Form.cleaned_data['password1']
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect(f'/')
        else:
            Form = SignUP()
        return render(request, 'registration/signup.html', {'form': Form})
    else:
        return redirect("/error")

@login_required
def profiles(request):
    if request.user.profile.type == "School":
        teachers = Profile.objects.filter(teacher__school = request.user.profile.name)
        
        context = {
            "teachers" : teachers
        }

        return render(request, 'profiles.html', context)
    else:
        return redirect('/Error')
@login_required
def profile(request, id):
    user = Profile.objects.get(id=id)
    if user.completed:
        if user == request.user.profile or user.type == "Teacher" and user.teacher.school == request.user.profile.name:
            if request.method == "POST":
                form = ProfileInfo(request.POST, request.Files, instance=user)
                if form.is_valid():
                    form.save()
                    return redirect("/")
            else:
                form = ProfileInfo(instance=user)
            
            context = {
                "form": form
            }

            return render(request, "edit_info.html", context)
        else:
            return redirect("/Error")
    else:
        if request.method == "POST":
            form = ProfileInfo(request.POST, request.FILES, instance=user)
            if form.is_valid:
                form.save()
                user.completed = True
                user.save()
        else:
            form = ProfileInfo(instance=user)

        context = {
            "form": form
        }    

        return render(request, "edit_info.html", context)