from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group, Permission, User


class Service(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название услуги")
    description = models.TextField(verbose_name="Описание услуги")
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name="Категория")  # Используем строку
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена", default=0)
    provider = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Поставщик услуги")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    location = models.CharField(max_length=100, default='', verbose_name="Город")

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")

    def __str__(self):
        return self.name



class Review(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.reviewer} for {self.service}"


class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  # Добавлено поле

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver}"

   
   
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='service_userprofile')
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.user.username
    
