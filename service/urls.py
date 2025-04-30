from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('service/', views.service_list, name='service_list'),
    path('service/<int:service_id>/', views.service_detail, name='service_detail'),
    path('service/create/', views.create_service, name='create_service'),
    path('service/<int:service_id>/add_review/', views.add_review, name='add_review'),
    path('send_message/<int:receiver_id>/', views.send_message, name='send_message'),
    path('chat/<int:receiver_id>/', views.chat, name='chat'),
]
