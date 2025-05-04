from django.shortcuts import render, redirect
from .forms import NewUserForm, UserProfileForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile

def register(request):
    if request.method == 'POST':
        user_form = NewUserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            # Создаем профиль пользователя
            UserProfile.objects.create(user=user, phone_number=user_form.cleaned_data['phone_number'])
            return redirect('login')  # Перенаправление на страницу входа после успешной регистрации
    else:
        user_form = NewUserForm()
    
    return render(request, 'registration/registration_page.html', {'user_form': user_form})


@login_required
def profile_view(request):
    try:
        profile = request.user.userprofile  # Предполагается, что у вас есть связь OneToOne с UserProfile
    except UserProfile.DoesNotExist:
        profile = None  # Профиль не найден

    return render(request, 'profile/profile.html', {'user': request.user, 'profile': profile})

@login_required
def edit_profile_view(request):
    try:
        profile = request.user.userprofile  # Проверяем, существует ли профиль
    except UserProfile.DoesNotExist:
        profile = None  # Профиль не найден, можно создать новый или обработать это иначе

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль успешно обновлен.")
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile) if profile else UserProfileForm()  # Если профиля нет, создаем пустую форму

    return render(request, 'profile/edit_profile.html', {'form': form})
