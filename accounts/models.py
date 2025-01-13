from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.utils import timezone
from datetime import timedelta

class CustomUser(AbstractUser):
    birth_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    tgusername = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=255,null=True, blank=True)
    leader = models.CharField(max_length=100, null=True, blank=True)
    role_position_user = models.CharField(max_length=100, null=True, blank=True, default=0)
    requisites = models.CharField(max_length=255, blank=True, null=True)
    first_sale = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    source_add = models.CharField(max_length=255, null=True, blank=True)
    profile_img = models.ImageField(upload_to="users/%Y/%m/%d/", default=None, null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    last_activity = models.DateTimeField(null=True, blank=True)
    role_user = models.CharField(max_length=100, null=True, blank=True, default=0)

   
    def __str__(self):
        return self.username 

    def save(self, *args, **kwargs):
        if not self.slug:  
            self.slug = slugify(self.username) 
        super().save(*args, **kwargs)

    def is_online(self):
        now = timezone.now()
        if self.last_activity:
            return now - self.last_activity < timedelta(minutes=5)  # 5 хвилин 
        return False
