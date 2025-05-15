from django.urls import path, include
from . import views
from service.views import service_detail_view, create_service  

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path("register/", views.register, name="register"),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('service/<int:service_id>/', service_detail_view, name='service_detail'),  # Исправлено
    path('service/new/', create_service, name='create_service'),  
]
