from django.urls import path, include
from . import views
from service.views import service_detail, create_service  # Импортируем из приложения service

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path("register/", views.register, name="register"),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('service/<int:service_id>/', service_detail, name='service_detail'),  # Используем service_detail из service
    path('service/new/', create_service, name='create_service'),  # Используем create_service из service
]
