from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Service, Review, Message, Category
from .forms import ServiceForm, ReviewForm, MessageForm
from django.db.models import Q
from django.contrib.auth import login




def home(request):
    service = Service.objects.all()
    categories = Category.objects.all()
    return render(request, 'service/home.html', {'service': service, 'categories': categories})

def service_list(request):
    services = Service.objects.all()  # Получаем все услуги из базы данных
    return render(request, 'service/service_list.html', {'services': services})

@login_required
def create_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.provider = request.user
            service.save()
            return redirect('home')
    else:
        form = ServiceForm()
    return render(request, 'service/create_service.html', {'form': form})


def service_detail(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    reviews = service.reviews.all()
    return render(request, 'service/service_detail.html', {'service': service, 'reviews': reviews})


@login_required
def add_review(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.service = service
            review.reviewer = request.user
            review.save()
            return redirect('service_detail', service_id=service.id)
    else:
        form = ReviewForm()
    return render(request, 'service/add_review.html', {'form': form, 'service': service})


@login_required
def send_message(request, receiver_id):
    receiver = get_object_or_404(User, id=receiver_id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = receiver
            message.save()
            return redirect('chat', receiver_id=receiver.id)
    else:
        form = MessageForm()
    return render(request, 'service/send_message.html', {'form': form, 'receiver': receiver})


@login_required
def chat(request, receiver_id):
    receiver = get_object_or_404(User, id=receiver_id)
    messages = Message.objects.filter(
        models.Q(sender=request.user, receiver=receiver) |
        models.Q(sender=receiver, receiver=request.user)
    ).order_by('timestamp')
    return render(request, 'service/chat.html', {'messages': messages, 'receiver': receiver})


def search(request):
    query = request.GET.get('q')
    category = request.GET.get('category')
    location = request.GET.get('location')

    service = Service.objects.all()

    if query:
        service = service.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    if category:
        service = service.filter(category__name__icontains=category)
    if location:
        service = service.filter(location__icontains=location)

    return render(request, 'service/home.html', {'service': service})
