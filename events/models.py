from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=100)
    image = models.ImageField(upload_to="event_images/", null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='events')

    def __str__(self):
        return self.name
    

class Participant(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    event = models.ManyToManyField(Event, related_name='participants')

    def __str__(self):
        return f"{self.name} - {self.email}"
    
