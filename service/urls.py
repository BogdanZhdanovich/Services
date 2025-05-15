from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('service/<int:service_id>/', views.service_detail_view, name='service_detail'),
    path('service/create/', views.create_service, name='create_service'),
    path('service/<int:service_id>/edit/', views.edit_service, name='edit_service'), 
    path('service/<int:service_id>/delete/', views.confirm_delete_service, name='confirm_delete_service'),
    path('service/<int:service_id>/add_review/', views.add_review, name='add_review'),
    path('send_message/<int:receiver_id>/', views.send_message, name='send_message'),
    path('message/<int:message_id>/', views.message_detail, name='message_detail'),

]
