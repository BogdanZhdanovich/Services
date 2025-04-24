from django import forms
from .models import Service, Review, Message
from django.contrib.auth.forms import UserCreationForm


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['title', 'description', 'category', 'price', 'image', 'location']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите название услуги'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите описание услуги'})
        self.fields['category'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Выберите категорию'})
        self.fields['price'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите цену'})
        self.fields['image'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Загрузите изображение'})
        self.fields['location'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите город'})


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating < 1 or rating > 5:
            raise ValidationError("Рейтинг должен быть от 1 до 5.")
        return rating

    def clean_comment(self):
        comment = self.cleaned_data.get('comment')
        if len(comment) > 500:
            raise ValidationError("Комментарий не должен превышать 500 символов.")
        return comment


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) > 1000:
            raise ValidationError("Сообщение не должно превышать 1000 символов.")
        return content
