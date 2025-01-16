from django.db import models
from accounts.models import *
from django.contrib.auth.models import Group
from sales.utils import generate_random_string
from transliterate import translit


class CategoriyChanels(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Channels(models.Model):
    name = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    category = models.ForeignKey(
        CategoriyChanels,
        on_delete=models.SET_NULL,
        related_name="cat_channels",
        null=True,
        blank=True,
    )
    slug = models.SlugField(max_length=100, unique=True)
    groups = models.ManyToManyField(Group, related_name="group_channels", blank=True)
    marker = models.BooleanField(default=False, blank=True)
    logo_channels = models.ImageField(upload_to="company/logo_channels/%Y/%m/%d/", default=None, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            num = 1
            base_slug = slugify(translit(self.name, "uk", reversed=True))[:255]

            while True:
                # Генерує унікальний slug з випадковим рядком
                random_string = generate_random_string()
                unique_slug = f"{base_slug}-{random_string}"

                # Перевіряє, чи існує вже такий slug
                if not Channels.objects.filter(slug=unique_slug).exists():
                    break
                num += 1

            self.slug = unique_slug[:255]  # Обмежити довжину до 255 символів
            print(self.slug)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ClientsCategoriy(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.name


class ClientsTypes(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    channel = models.ForeignKey(Channels, null=True, blank=True, on_delete=models.SET_NULL, related_name="ch")
    tariff = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    category = models.ForeignKey(ClientsCategoriy, on_delete=models.SET_NULL, null=True, default=1)
    types = models.ForeignKey(ClientsTypes, on_delete=models.SET_NULL, null=True, default=1)
    payment_in = models.CharField(max_length=255, blank=True, null=True)
    date_payment = models.DateField(blank=True, null=True)
    date_post = models.DateField(blank=True, null=True)
    time_post = models.TimeField(blank=True, null=True)
    scrin = models.ImageField(upload_to="screenshots/%Y/%m/%d/", default=None, null=True, blank=True)
    posts_text = models.TextField(blank=True, null=True)
    sales = models.ForeignKey(
        CustomUser,
        related_name="sales_posts",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    content = models.ForeignKey(
        CustomUser,
        related_name="content_posts",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    slug = models.SlugField(max_length=255)
    status = models.BooleanField(default=False, null=True, blank=True)


class PostChannel(models.Model):
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True, blank=True)
    channel = models.ForeignKey(Channels, on_delete=models.SET_NULL, null=True, blank=True)
    time_post = models.TimeField(blank=True, null=True)
    tarif = models.CharField(max_length=255, blank=True, null=True)
    date_post = models.DateField(blank=True, null=True)
    status_write = models.BooleanField(default=False, null=True, blank=True)
    content_update = models.ForeignKey(
        "accounts.CustomUser",
        related_name="content_update_postchannels",
        on_delete=models.DO_NOTHING,
        default=None,
        null=True,
        blank=True,
    )
    channels_slug = models.SlugField(max_length=255)

    def __str__(self):
        return f"{self.channel.name}"
