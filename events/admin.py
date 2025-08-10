from django.contrib import admin
from events.models import Event, Category, CustomUser

# Register your models here.

admin.site.register(Event)
admin.site.register(Category)
admin.site.register(CustomUser)
