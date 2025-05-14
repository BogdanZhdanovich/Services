from django.shortcuts import render, redirect
from .forms import NewUserForm, UserProfileForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from service.models import Service

def register(request):
    if request.method == 'POST':
        user_form = NewUserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password1'])  
            user.save()  
            
            UserProfile.objects.create(
                user=user,
                phone_number=user_form.cleaned_data['phone_number'], 
                first_name=user_form.cleaned_data['first_name'],
                last_name=user_form.cleaned_data['last_name']
            )
            messages.success(request, 'Регистрация прошла успешно! Вы можете войти в систему.')
            login(request, user)  
            return redirect('profile') 
    else:
        user_form = NewUserForm()

    return render(request, 'registration/registration_page.html', {'user_form': user_form})

@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)  
    services = Service.objects.filter(provider=request.user)  

    return render(request, 'profile/profile.html', {
        'user': request.user,
        'profile': profile,
        'services': services,  
    })

@login_required
def edit_profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)  

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save() 
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('profile')  
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'profile/edit_profile.html', {'form': form})
