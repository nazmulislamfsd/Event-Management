import debug_toolbar
from django.conf import settings
from django.urls import path, include
from django.contrib import admin
from events.views import home

urlpatterns = [
    path("", home, name='home'),
    path('admin/', admin.site.urls),
    path('event/', include('events.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
