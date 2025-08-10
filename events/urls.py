
from django.urls import path
from events.views import CreateEvent, CreateCategory, create_participant, view_event, delete_event, delete_category, delete_participant, update_event, update_category, update_participant, dashboard, details, create_group, delete_group, change_role, no_permission,rsvp_system, activate_user
from events.views import SignIn, SignOut, SignUp, Profile, EditProfile, CustomPasswordChangeView, CustomPasswordChangeDoneView, CustomPasswordResetView, CustomPasswordResetConfirmView
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, PasswordResetDoneView


urlpatterns = [
    # path('create-event/', create_event, name='create-event'),
    path('create-event/', CreateEvent.as_view(), name='create-event'),
    # path('create-category/', create_category, name='create-category'),
    path('create-category/', CreateCategory.as_view(), name='create-category'),
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
    # path('sign-up/', signUp, name='sign-up'),
    path('sign-up/', SignUp.as_view(), name='sign-up'),
    # path('sign-in/', signIn, name='sign-in'),
    path('sign-in/', SignIn.as_view(), name='sign-in'),
    # path('sign-out/', signOut, name='sign-out'),
    path('sign-out/', SignOut.as_view(), name='sign-out'),
    path('create-group/', create_group, name='create-group'),
    path('delete-group/<int:id>/', delete_group, name='delete-group'),
    path('change-role/<int:id>/', change_role, name='change-role'),
    path('no-permission/', no_permission, name='no-permission'),
    path('rsvp-system/<int:id>/', rsvp_system, name='rsvp-system'),
    path('activate/<int:user_id>/<str:token>/', activate_user, name='activate-user'),
    path('user/profile/', Profile.as_view(), name='profile'),
    path('user/edit/profile/', EditProfile.as_view(), name='edit-profile'),
    path('user/password-change/', CustomPasswordChangeView.as_view(), name='password-change'),
    path('user/password-change-done/', CustomPasswordChangeDoneView.as_view(), name='password_change_done'),
    path('user/password-reset/', CustomPasswordResetView.as_view(), name='password-reset'),
    path('user/password-reset-done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),

]
