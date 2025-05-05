from django.urls import path, include
from . import views
from .views import profile_view, edit_profile_view

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path("register/", views.register, name="register"),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', edit_profile_view, name='edit_profile'),
]
