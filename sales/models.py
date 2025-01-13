from typing import Any
from django.db import models
from django.utils.text import slugify
from transliterate import translit
from accounts.models import CustomUser
from django.contrib.auth import get_user_model
from sales.utils import generate_random_string

CustomUser = get_user_model()


class ClientStatus(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    
    def __str__(self):
        return self.name




class Clients(models.Model):
    date = models.DateField(max_length=100)
    where = models.CharField(max_length=100)
    category = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    salary = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    social_media = models.CharField(max_length=255)
    phones = models.CharField(max_length=255, blank=True, null=True) 
    link = models.TextField(max_length=255, blank=True)
    block = models.BooleanField(blank=True, null=True)
    status = models.ForeignKey(ClientStatus, on_delete=models.SET_NULL, null=True, default=1)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    data_processing = models.DateTimeField(null=True, blank=True)
    answer = models.BooleanField(null=True, blank=True)
    date_the_first_buys = models.DateTimeField(null=True, blank=True)
    date_last_buys = models.DateTimeField(null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    clients_cost = models.IntegerField(null=True, blank=True)
    sales_manager = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    comment = models.TextField(blank=True, null=True)
    process = models.BooleanField(null= True, blank=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            num = 1
            base_slug = slugify(translit(self.title, 'uk', reversed=True))[:255]

            while True:
                # Генерує унікальний slug з випадковим рядком
                random_string = generate_random_string()
                unique_slug = f"{base_slug}-{random_string}"
                
                # Перевіряє, чи існує вже такий slug
                if not Clients.objects.filter(slug=unique_slug).exists():
                    break
                num += 1

            self.slug = unique_slug[:255]  # Обмежити довжину до 255 символів
            print(self.slug)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.title

