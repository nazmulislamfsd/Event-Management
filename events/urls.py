
from django.urls import path
from events.views import create_event, create_category, create_participant, view_event, view_category, view_participant, delete_event, delete_category, delete_participant, update_event, update_category, update_participant, dashboard


urlpatterns = [
    path('create-event/', create_event, name='create-event'),
    path('create-category/', create_category, name='create-category'),
    path('create-participant/', create_participant, name='create-participant'),
    path('view-event/', view_event, name='view-event'),
    path('view-category/', view_category, name='view-category'),
    path('view-participant/', view_participant, name='view-participant'),
    path('delete-event/<int:id>/', delete_event, name='delete-event'),
    path('delete-category/<int:id>/', delete_category, name='delete-category'),
    path('delete-participant/<int:id>/', delete_participant, name='delete-participant'),
    path('update-event/<int:id>/', update_event, name='update-event'),
    path('update-category/<int:id>/', update_category, name='update-category'),
    path('update-participant/<int:id>/', update_participant, name='update-participant'),
    path('dashboard/', dashboard, name='dashboard')
]
