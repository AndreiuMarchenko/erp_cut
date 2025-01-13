from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser



class UserAuth(AuthenticationForm):
    username = forms.CharField(label="Логін", widget=forms.TextInput(attrs={'class' : 'form-control'}))
    password = forms.CharField(label="Введіть пароль", widget=forms.PasswordInput(attrs={'class' : 'form-control'}))

    class Meta:
        model = CustomUser
        

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={'class' : 'form-control'}))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class' : 'form-control'}))
    password2 = forms.CharField(label="Підтвердіть пароль", widget=forms.PasswordInput(attrs={'class' : 'form-control'}))
    first_sale = forms.ChoiceField(choices=[], label="Перший продаж", required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    paid = forms.ChoiceField(choices=[], label="Оплачено", required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    source_add = forms.CharField(label="Джерело", required=False, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    profile_img = forms.ImageField(label="Вибір фотографії", required=False, widget=forms.FileInput(attrs={'class' : ' form-control', 'id' : 'inputGroupFile02'}))
    username = forms.CharField(
        label="Змінити логін",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'custom_arg': 'Логін для входу', 'placeholder': 'username'})
    )
    first_name = forms.CharField(label="Змінити Імʼя", required=False, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'Катерина'}))
    last_name = forms.CharField(label="Змінити Прізвище", required=False, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'Кравченко'}))
    birth_date = forms.DateField(label="Дата народження", input_formats=['%m/%d/%Y', '%Y-%m-%d'], required=False, widget=forms.TextInput(attrs={'class' : 'form-control', 'id': 'dp1', 'placeholder': '03/06/1999'}))
    phone = forms.CharField(label="Номер телефону", 
                            required=False, 
                            widget=forms.TextInput(attrs={'class' : 'form-control', 'id': 'phone', 'custom_arg': '+380',}))
    tgusername = forms.CharField(label="Телеграм аккаунт", required=False, widget=forms.TextInput(attrs={'class' : 'form-control', 'custom_arg': '@'}))
    address = forms.CharField(label="Адреса проживання", required=False, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'Місто Київ'}))
    requisites = forms.CharField(label="Реквізити", required=False, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)


        data = [(1, "Так"), (0, "Ні")]
        self.fields['first_sale'].choices = data
        self.fields['paid'].choices = data

    class Meta:
        model = CustomUser


        fields = ['username', 'password1', 'password2', 'birth_date',
                  'first_name', 'last_name', 
                  'profile_img',
                   'first_sale',
                  'paid', 'source_add',
                  'requisites',
                   'phone', 'tgusername', 'address']

        widgets = {
            'position': forms.Select(attrs={'class': 'form-control'}),
            
        }
        labels = {
            'position': 'Позиція',
        }

