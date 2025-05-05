from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
import logging
from .models import Service, Review, Message, Category
from .forms import ServiceForm, ReviewForm, MessageForm

logger = logging.getLogger(__name__)

def home(request):
    services = Service.objects.select_related('provider').all()  # Используем select_related для оптимизации
    categories = Category.objects.all()
    return render(request, 'service/home.html', {'services': services, 'categories': categories})

def service_list(request):
    services = Service.objects.all()
    paginator = Paginator(services, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'service/service_list.html', {'page_obj': page_obj})

@login_required
def create_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.provider = request.user  # Установка текущего пользователя как провайдера
            service.save()
            return redirect('service_list')  # Переход на страницу списка услуг
    else:
        form = ServiceForm()
    return render(request, 'service/create_service.html', {'form': form})

def service_detail(request, service_id):
    service = get_object_or_404(Service.objects.select_related('provider'), id=service_id)
    reviews = service.reviews.select_related('reviewer').all()
    return render(request, 'service/service_detail.html', {'service': service, 'reviews': reviews})

@login_required
def add_review(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.user == service.provider:
        return HttpResponseForbidden("Вы не можете оставить отзыв на свою услугу.")
    
    form = ReviewForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        review = form.save(commit=False)
        review.service = service
        review.reviewer = request.user
        review.save()
        logger.info(f"Отзыв на услугу '{service.title}' добавлен пользователем {request.user.username}.")
        return redirect('service_detail', service_id=service.id)
    
    return render(request, 'service/add_review.html', {'form': form, 'service': service})

@login_required
def send_message(request, receiver_id):
    receiver = get_object_or_404(User, id=receiver_id)
    form = MessageForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        message = form.save(commit=False)
        message.sender = request.user
        message.receiver = receiver
        message.save()
        logger.info(f"Сообщение отправлено от {request.user.username} к {receiver.username}.")
        return redirect('chat', receiver_id=receiver.id)
    
    return render(request, 'service/send_message.html', {'form': form, 'receiver': receiver})

@login_required
def chat(request, receiver_id):
    receiver = get_object_or_404(User, id=receiver_id)
    messages = Message.objects.filter(
        Q(sender=request.user, receiver=receiver) |
        Q(sender=receiver, receiver=request.user)
    ).order_by('timestamp')
    return render(request, 'service/chat.html', {'messages': messages, 'receiver': receiver})

def search(request):
    query = request.GET.get('q', '')
    category_name = request.GET.get('category', '')
    location = request.GET.get('location', '')

    services = Service.objects.select_related('provider').all()  # Используем select_related для оптимизации

    if query:
        services = services.filter(title__icontains=query)
    if category_name:
        services = services.filter(category__name__icontains=category_name)
    if location:
        services = services.filter(location__icontains=location)

    # Пагинация
    paginator = Paginator(services, 10)  # 10 услуг на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    return render(request, 'service/search_results.html', {
        'services': page_obj,  # Передаем page_obj вместо services
        'query': query,
        'categories': categories,
        'page_obj': page_obj,  # Передаем page_obj в контекст
    })

