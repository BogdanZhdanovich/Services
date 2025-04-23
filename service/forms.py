from django import forms
from .models import Service, Review, Message
from django.contrib.auth.forms import UserCreationForm


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['title', 'description', 'category', 'location']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']

