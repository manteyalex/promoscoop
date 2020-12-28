from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField()
    subscribed = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    region = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.user.username} Profile'