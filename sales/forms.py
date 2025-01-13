from post.models import ClientsCategoriy

from django import forms
from sales.models import Clients
from accounts.models import CustomUser



 
class AddClientsForms(forms.ModelForm):
    title = forms.CharField(label="Назва", required=False, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'Менеджер з продажу'}))
    salary = forms.CharField(label="Заробітна плата", required=False, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder': '10 000 грн'}))
    city = forms.CharField(label="Місто", required=False, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'Київ'}))
    social_media = forms.CharField(label="Соціальні мережі", required=True, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'https://t.me/username'}))
    phones = forms.CharField(label="Номер телефону", required=False, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder': '+380 '}))
    link = forms.CharField(label="Посилання", required=False, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'https://t.me/channel_name'}))
    category = forms.ChoiceField(label="Категорія", required=False, choices=[], widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'SMM'}))

    class Meta:
        model = Clients
        fields = ['category', 'title', 'salary', 'city', 'social_media', 'phones', 'link']
        labels = {
            'category': 'Категорія',
            'sales_manager': 'Sales',

        }
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),

        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Витягуємо користувача
        super().__init__(*args, **kwargs)
        cat_choices = [(cat.id, cat.name) for cat in ClientsCategoriy.objects.all()]
        self.fields['category'].choices = cat_choices






