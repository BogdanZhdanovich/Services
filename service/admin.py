from django.contrib import admin
from .models import Service, Category, Review, Message, UserProfile


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'provider', 'created_at')  
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'description')  

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',) 
    search_fields = ('name',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('service', 'reviewer', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('comment',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('content',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')  
    search_fields = ('user__username', 'phone_number')  
