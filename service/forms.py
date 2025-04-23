from django import forms
from .models import Service, Review, Message
from django.core.exceptions import ValidationError

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['title', 'category', 'location', 'description', 'price']
        

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise forms.ValidationError("Цена не может быть отрицательной.")
        return price


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
