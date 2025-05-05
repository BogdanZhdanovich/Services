from django.contrib import admin
from .models import Service, Category, Review, Message, UserProfile

# Регистрация модели Service
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'provider', 'created_at')  # Поля, отображаемые в списке
    list_filter = ('category', 'created_at')  # Фильтры
    search_fields = ('title', 'description')  # Поиск по полям

# Регистрация модели Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

# Регистрация модели Review
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('service', 'reviewer', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('comment',)

# Регистрация модели Message
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('content',)

# Регистрация модели UserProfile
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')  # Поля, отображаемые в списке
    search_fields = ('user__username', 'phone_number')  # Поиск по полям
