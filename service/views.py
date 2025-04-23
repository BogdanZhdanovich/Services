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
    services = Service.objects.all()
    categories = Category.objects.all()
    return render(request, 'service/home.html', {'services': services, 'categories': categories})

def service_list(request):
    services = Service.objects.all()
    paginator = Paginator(services, 10)  # 10 услуг на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'service/service_list.html', {'page_obj': page_obj})

@login_required
def create_service(request):
    try:
        if request.method == 'POST':
            form = ServiceForm(request.POST)
            if form.is_valid():
                service = form.save(commit=False)
                service.provider = request.user
                service.save()
                logger.info(f"Услуга '{service.title}' создана пользователем {request.user.username}.")
                return redirect('home')
        else:
            form = ServiceForm()
        return render(request, 'service/create_service.html', {'form': form})
    except Exception as e:
        logger.error(f"Ошибка при создании услуги: {e}")
        return render(request, 'service/error.html', {'message': 'Произошла ошибка при создании услуги.'})

def service_detail(request, service_id):
    service = get_object_or_404(Service.objects.select_related('provider'), id=service_id)
    reviews = service.reviews.select_related('reviewer').all()
    return render(request, 'service/service_detail.html', {'service': service, 'reviews': reviews})

@login_required
def add_review(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.user == service.provider:
        return HttpResponseForbidden("Вы не можете оставить отзыв на свою услугу.")
    try:
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
    except Exception as e:
        logger.error(f"Ошибка при добавлении отзыва: {e}")
        return render(request, 'service/error.html', {'message': 'Произошла ошибка при добавлении отзыва.'})

@login_required
def send_message(request, receiver_id):
    receiver = get_object_or_404(User, id=receiver_id)
    try:
        if request.method == 'POST':
            form = MessageForm(request.POST)
            if form.is_valid():
                message = form.save(commit=False)
                message.sender = request.user
                message.receiver = receiver
                message.save()
                logger.info(f"Сообщение отправлено от {request.user.username} к {receiver.username}.")
                return redirect('chat', receiver_id=receiver.id)
        else:
            form = MessageForm()
        return render(request, 'service/send_message.html', {'form': form, 'receiver': receiver})
    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения: {e}")
        return render(request, 'service/error.html', {'message': 'Произошла ошибка при отправке сообщения.'})

@login_required
def chat(request, receiver_id):
    receiver = get_object_or_404(User, id=receiver_id)
    messages = Message.objects.filter(
        Q(sender=request.user, receiver=receiver) |
        Q(sender=receiver, receiver=request.user)
    ).order_by('timestamp')
    return render(request, 'service/chat.html', {'messages': messages, 'receiver': receiver})

def search(request):
    query = request.GET.get('q')
    category = request.GET.get('category')
    location = request.GET.get('location')

    logger.info(f"Поисковый запрос: query={query}, category={category}, location={location}")

    services = Service.objects.all()

    if not (query or category or location):
        return render(request, 'service/search_results.html', {'page_obj': None, 'query': query})

    if query:
        services = services.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    if category:
        services = services.filter(category__name__icontains=category)
    if location:
        services = services.filter(location__icontains=location)

    paginator = Paginator(services, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'service/search_results.html', {'page_obj': page_obj, 'query': query})
