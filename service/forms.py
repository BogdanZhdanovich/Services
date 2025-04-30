from django import forms
from .models import Service, Review, Message
from django.core.exceptions import ValidationError

class ServiceForm(forms.ModelForm):
    PRICE_CHOICES = [
        ('fixed', 'Фиксированная цена'),
        ('contract', 'Договорная цена'),
    ]
    
    price_type = forms.ChoiceField(
        choices=PRICE_CHOICES,
        widget=forms.RadioSelect,
        label='Тип цены',
        initial='fixed'  # Установить фиксированную цену по умолчанию
    )

    price = forms.DecimalField(required=False, label='Цена', widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите цену',
        'style': 'width: 150px;'  # Устанавливаем меньшую ширину
    }))

    class Meta:  # Исправленный отступ
        model = Service
        fields = ['title', 'description', 'category', 'price_type', 'price', 'location']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите название услуги'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите описание услуги'})
        self.fields['category'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Выберите категорию'})
        self.fields['price_type'].widget.attrs.update({'class': 'form-check-input'})  # Для радио-кнопок
        self.fields['price'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите цену'})
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
