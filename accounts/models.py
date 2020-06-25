from django.db import models
from django.contrib.auth.models import User

import datetime
from django.conf import settings
from django.core.cache import cache

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    age = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.user}'

