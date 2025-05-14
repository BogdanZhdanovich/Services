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
    services = Service.objects.select_related('provider').all()
    paginator = Paginator(services, 9)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    return render(request, 'service/home.html', {'services': page_obj, 'categories': categories})

@login_required
def create_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.provider = request.user 
            service.save()
            logger.info(f"Услуга '{service.title}' успешно создана пользователем {request.user.username}.")
            return redirect('home') 
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

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.service = service
            review.reviewer = request.user
            review.save()
            logger.info(f"Отзыв на услугу '{service.title}' добавлен пользователем {request.user.username}.")
            return redirect('service_detail', service_id=service.id)
    else:
        form = ReviewForm()

    return render(request, 'service/add_review.html', {'form': form, 'service': service})

@login_required
def send_message(request, receiver_id):
    receiver = get_object_or_404(User, id=receiver_id)
    form = MessageForm()  # Инициализация формы
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
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

    logger.debug(f"Search query: {query}, Category: {category_name}, Location: {location}")

    services = Service.objects.select_related('provider')

    if query:
        services = services.filter(title__icontains=query)
    if category_name:
        services = services.filter(category__icontains=category_name)  # Исправлено здесь
    if location:
        services = services.filter(location__icontains=location)

    logger.debug(f"Filtered services count: {services.count()}")

    paginator = Paginator(services, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    return render(request, 'service/search_results.html', {
        'services': page_obj,
        'query': query,
        'categories': categories,
    })


@login_required
def edit_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    
    if request.user != service.provider:
        return HttpResponseForbidden("Вы не можете редактировать эту услугу.")

    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            logger.info(f"Услуга '{service.title}' была обновлена пользователем {request.user.username}.")
            return redirect('service_detail', service_id=service.id)
    else:
        form = ServiceForm(instance=service)
    
    return render(request, 'service/service_edit.html', {'form': form, 'service': service})


@login_required
def confirm_delete_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    
    if request.user != service.provider:
        return HttpResponseForbidden("Вы не можете удалить эту услугу.")

    if request.method == 'POST':
        service.delete()
        logger.info(f"Услуга '{service.title}' была удалена пользователем {request.user.username}.")
        return redirect('home')  # Или на другую страницу, например, на страницу со списком услуг
    
    return render(request, 'service/service_confirm_delete.html', {'service': service})


@login_required
def profile_view(request):
    user = request.user
    profile = user.profile  # Предположим, что у вас есть профиль
    services = user.services.all()  # Получите услуги пользователя

    # Получите непрочитанные сообщения
    unread_messages = user.received_messages.filter(is_read=False)

    context = {
        'user': user,
        'profile': profile,
        'services': services,
        'unread_messages': unread_messages,
    }
    
    return render(request, 'profile.html', context)


@login_required
def message_detail(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if request.user not in [message.sender, message.receiver]:
        return HttpResponseForbidden("Вы не имеете доступа к этому сообщению.")
    
    # Обновление статуса сообщения как прочитанное
    message.is_read = True
    message.save()
    
    return render(request, 'service/message_detail.html', {'message': message})


def chat_list(request):
    # Получаем всех пользователей, с которыми есть переписка
    users = User.objects.filter(
        Q(message__sender=request.user) | Q(message__receiver=request.user)
    ).distinct()

    return render(request, 'service/chat_list.html', {'users': users})