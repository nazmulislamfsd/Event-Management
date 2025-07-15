
from django.urls import path
<<<<<<< HEAD
from events.views import create_event, create_category, create_participant, view_event, delete_event, delete_category, delete_participant, update_event, update_category, update_participant, dashboard, details

=======
from events.views import create_event, create_category, create_participant, view_event, delete_event, delete_category, delete_participant, update_event, update_category, update_participant, dashboard, details, create_group, delete_group, change_role, no_permission,rsvp_system, activate_user
from events.views import signUp, signIn, signOut
>>>>>>> assignment-2

urlpatterns = [
    path('create-event/', create_event, name='create-event'),
    path('create-category/', create_category, name='create-category'),
    path('create-participant/', create_participant, name='create-participant'),
    path('view-event/', view_event, name='view-event'),
    path('delete-event/<int:id>/', delete_event, name='delete-event'),
    path('delete-category/<int:id>/', delete_category, name='delete-category'),
    path('delete-participant/<int:id>/', delete_participant, name='delete-participant'),
    path('update-event/<int:id>/', update_event, name='update-event'),
    path('update-category/<int:id>/', update_category, name='update-category'),
    path('update-participant/<int:id>/', update_participant, name='update-participant'),
    path('dashboard/', dashboard, name='dashboard'),
    path('details/<int:id>/', details, name='details'),
<<<<<<< HEAD
=======
    path('sign-up/', signUp, name='sign-up'),
    path('sign-in/', signIn, name='sign-in'),
    path('sign-out/', signOut, name='sign-out'),
    path('create-group/', create_group, name='create-group'),
    path('delete-group/<int:id>/', delete_group, name='delete-group'),
    path('change-role/<int:id>/', change_role, name='change-role'),
    path('no-permission/', no_permission, name='no-permission'),
    path('rsvp-system/<int:id>/', rsvp_system, name='rsvp-system'),
    path('activate/<int:user_id>/<str:token>/', activate_user, name='activate-user')

>>>>>>> assignment-2
]
