from django import forms
from .models import Post, PostChannel, Channels, CategoriyChanels
import datetime
from django.contrib.auth.models import Group
from django.forms import ModelForm



from django.forms.models import inlineformset_factory


class AddPostForm(forms.ModelForm):
    date_payment = forms.DateField(label="Дата оплати", input_formats=['%d/%m/%Y', '%Y-%m-%d'], required=False, 
                                   widget=forms.TextInput(attrs={'class': 'form-control datepicker',  'name' : 'date-pay',
                                                                 'autocomplete': 'off',  
                                                                 'value': f'{datetime.datetime.now().strftime("%d/%m/%Y")}', 'id' : 'date-formatting2'}))

    scrin = forms.ImageField(label="Скріншот підтвердження", required=False, 
                             widget=forms.FileInput(attrs={'class': 'form-control'}))
    posts_text = forms.Textarea()

    class Meta:
        model = Post
        fields = ['category', 'types', 'payment_in', 'date_payment', 'scrin', 'posts_text']

        data = [(1, "Карта"), (0, "Крипта"), (2, "Рахунок"), (3, "Рахунок євро"), (4, "Рахунок доллар"), (5, "PayPal Євро"), (6, "PayPal Доллар")]
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'types': forms.Select(attrs={'class': 'form-select'}),
            'payment_in': forms.Select(choices=data, attrs={'class': 'form-select'}),
            'posts_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5,'id':'msgCustomer'}),
        }
        labels = {
            'category': 'Категорія',
            'types': 'Тип',
            'payment_in': 'Оплата',
            'posts_text': 'Текст публікації',
        }



class AddPostToChannelsForm(forms.ModelForm):
    date_post = forms.DateField(
        label="Дата публікації", 
        input_formats=['%d/%m/%Y', '%Y-%m-%d'], 
        required=False, 
        widget=forms.TextInput(attrs={
            'class': 'form-control date-field', 
            'autocomplete': 'off',
            'name': 'date_post',
            'id' : 'datepicker-0',
            'placeholder': 'dd/MM/YYYY'
        })
    )


    class Meta:
        model = PostChannel
        fields = ['channel', 'time_post', 'date_post', 'tarif', 'post']
        widgets = {
            'channel': forms.Select(attrs={'class': 'form-select', 'name' : 'channel'}),
            'time_post': forms.TimeInput(attrs={'class': 'form-control time-field', 'name': 'time_post', 'autocomplete': 'off', 'placeholder' : 'HH:MM', 'id': 'hm-0'}),
            'tarif': forms.TextInput(attrs={'class': 'form-control', 'name': 'tarif', 'autocomplete': 'off'}),
            'post': forms.HiddenInput()
        }
        labels = {
            'channel': 'Обрати канал',
            'time_post': 'Час публікації',
            'tarif': 'Тариф'
        }
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None) 
        super().__init__(*args, **kwargs)
        
        if user:
            
            channels = Channels.objects.select_related('category').all().order_by('-category__id')

            self.fields['channel'].queryset = channels
        else:
            self.fields['channel'].queryset = Channels.objects.none()


            
        self.fields['channel'].label_from_instance = self.label_from_instance


    def label_from_instance(self, obj):
            # """Додаємо 'новий канал', якщо marker=True."""
            return f"{obj.name} ({obj.category}) (новий)" if obj.marker else f"{obj.name} ({obj.category})"

def PostChannelFormSet(*args, **kwargs):
    user = kwargs.pop('user', None)

    formset = inlineformset_factory(Post, PostChannel, 
                                    form=AddPostToChannelsForm, 
                                    can_delete=True,
                                    extra=1)(*args, **kwargs)

    for form in formset:
        form.fields['channel'].queryset = form.fields['channel'].queryset.none()  # Спочатку обнуляємо
        
        form.user = user
        form.__init__(*args, user=user, **kwargs)  # Передаємо користувача під час ініціалізації

    
    return formset



class AddNewChannel(ModelForm):
    name = forms.CharField(label="Назва каналу", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    link = forms.CharField(label="Посилання на канал", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Channels
        fields = ['name', 'link', 'category', 'groups']

        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'groups': forms.CheckboxSelectMultiple(),  # Використовуємо чекбокси для багатьох виборів
        }
        labels = {
            'category': 'Категорія каналу',
            'groups': 'Групи',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categoriy_choices = [(category.id, category.name) for category in CategoriyChanels.objects.all()]
        groups_choices = [(group.id, group.name) for group in Group.objects.all()] 

        self.fields['category'].choices = categoriy_choices
        self.fields['groups'].choices = groups_choices









class ChannelForm(forms.ModelForm):
    name = forms.CharField(
        label='Назва каналу', 
        max_length=255, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    link = forms.CharField(
        label='Посилання на канал', 
        max_length=255, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    category = forms.ChoiceField(
        label='Категорія',
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Channels
        fields = ['name', 'link', 'category']

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            category_choices = CategoriyChanels.objects.values_list('id', 'name')  # Отримання ID та імен категорій
            self.fields['category'].choices = [('', '--- Оберіть категорію ---')] + [(id, name) for id, name in category_choices]

    def clean_category(self):
            category_id = self.cleaned_data.get('category')
            if category_id:
                return CategoriyChanels.objects.get(id=category_id)
            return None