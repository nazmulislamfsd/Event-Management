from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

'''Custom User Model'''
class CustomUser(AbstractUser):
    profile_image = models.ImageField(upload_to='profileImages', blank=True, default='profileImages/default.png')
    bio = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.username

'''Create your models here.'''

class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='rsvp_events')
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=100)
    image = models.ImageField(upload_to="event_images/", null=True, blank=True, default="Event_images/default.jpg")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='events')

    def __str__(self):
        return self.name
    