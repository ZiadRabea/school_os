from django.urls import path
from.views import sign_up, profiles, profile

urlpatterns = [
    path('signup/', sign_up),
    path('teachers/<int:id>/signup_teacher/', sign_up),
    path('profiles/', profiles),
    path('profile/<int:id>', profile)
]