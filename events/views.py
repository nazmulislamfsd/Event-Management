from django.shortcuts import render, redirect, HttpResponse
from events.forms import EventModelForm, CategoryModelForm, GroupModelForm, CustomSignUpModelForm, SignInForm, ChangeRoleForm, EditProfileForm, CustomPasswordChangeForm, CustomPasswordResetForm, CustomPasswordResetConfirmForm
from events.models import Event, Category
from django.contrib import messages
from datetime import date
from django.contrib.auth import login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib.auth.tokens import default_token_generator
from django.views.generic import TemplateView, CreateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.views import View
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model

User = get_user_model()

'''Role access'''

def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def is_organizer(user):
    return user.groups.filter(name='Organizer').exists()

'''Create your views here.'''

'''
def home(request):
    base_query = Event.objects.prefetch_related('category').prefetch_related('participants')
    events = Event.objects.prefetch_related('category').filter(date=date.today()).prefetch_related('participants')

    query = request.GET.get('q')

    if query:
        events = base_query.filter(name__icontains=query)

    return render(request, 'home.html', {'events':events})

'''

class Home(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        base_query = Event.objects.prefetch_related('category').prefetch_related('participants')
        query = self.request.GET.get('q')
        if query:
            context['events'] = base_query.filter(name__icontains=query)
        else:
            context['events'] = Event.objects.prefetch_related('category').filter(date=date.today()).prefetch_related('participants')
        
        return context
    

@login_required
@user_passes_test(is_admin, login_url='no-permission')
def create_group(request):
    form = GroupModelForm()

    if request.method == "POST":
        form = GroupModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Group Created")
            return redirect('dashboard')
        
    return render(request, 'group_form.html', {'form':form})


'''
@login_required
@permission_required("events.add_event", login_url='no-permission')
def create_event(request):
    form = EventModelForm()

    if request.method == 'POST':
        form = EventModelForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()

            messages.success(request, "Successfully Created Event")
            return redirect('dashboard')

    return render(request, 'create_event.html', {'form':form})

'''

create_event_decorator = [login_required, permission_required('events.add_event', login_url='no-permission')]
@method_decorator(create_event_decorator, name='dispatch')
class CreateEvent(CreateView):
    model = Event
    form_class = EventModelForm
    template_name = 'create_event.html'
    success_url = reverse_lazy('dashboard')

    def get_success_url(self):
        messages.success(self.request, "Successfully Created Event.")
        return reverse_lazy('dashboard')
    

'''
@login_required
@permission_required('events.add_category', login_url='no-permission')
def create_category(request):
    form = CategoryModelForm()

    if request.method == 'POST':
        form = CategoryModelForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Created Category")
            return redirect('dashboard')

    return render(request, 'create_category.html', {'form':form})

'''

create_category_decorator = [login_required, permission_required('events.add_category', login_url='no-permission')]
@method_decorator(create_category_decorator, name='dispatch')
class CreateCategory(CreateView):
    model = Category
    form_class = CategoryModelForm
    template_name = 'create_category.html'

    def get_success_url(self):
        messages.success(self.request, "Successfully Created Category.")
        return reverse_lazy('dashboard')

    

@login_required
@user_passes_test(is_admin, login_url='no-permission')
def create_participant(request):
    form = CustomSignUpModelForm()

    if request.method == 'POST':
        form = CustomSignUpModelForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password1'))
            user.is_active = False
            user.save()

            messages.success(request, "Successfully Created Participant")
            return redirect('dashboard')
    
    return render(request, 'signUp.html', {'form':form})


@login_required
def view_event(request):
    events = Event.objects.prefetch_related('category').prefetch_related('participants')

    query = request.GET.get('q')

    if query:
        categorys = Category.objects.filter(name__icontains=query)
        if categorys:
            category = categorys.first()
            events = Event.objects.prefetch_related('category').filter(category=category).prefetch_related('participants')
        else:
            messages.error(request, "No category matching!!")
            return redirect('view-event')
    
    startDate = request.GET.get('a')
    endDate = request.GET.get('b')

    if startDate and endDate: 
        events = Event.objects.prefetch_related('category').prefetch_related('participants').filter(date__gte=startDate).filter(date__lte=endDate)
        
    return render(request, 'view_event.html', {'events':events})

@login_required
def dashboard(request):

    # base_query = Event.objects.prefetch_related('category').prefetch_related('participants')
    events = Event.objects.prefetch_related('category').prefetch_related('participants')
    group = request.user.groups.first()
    if group:
        user_group_name = group.name 
    else:
        user_group_name = None

    type = request.GET.get('type','all')
    if type=='totalParticipants':
        title = "total participants"
        participants = User.objects.filter(rsvp_events__isnull=False).distinct()
        # participants = User.objects.all()
        events = ""
        categorys = ""
        groups = ""
    elif type=='totalCategorys':
        title = "total categorys"
        categorys = Category.objects.all()
        events = ""
        participants = ""
        groups = ""
    elif type=='upComingEvents':
        title = "up coming events"
        events = Event.objects.prefetch_related('category').prefetch_related('participants').filter(date__gt=date.today())
        participants = ""
        categorys = ""
        groups = ""
    elif type=='pastEvents':
        title = "past events"
        events = Event.objects.prefetch_related('category').prefetch_related('participants').filter(date__lt=date.today())
        participants = ""
        categorys = ""
        groups = ""
    elif type=='all':
        title = "all events"
        events = Event.objects.prefetch_related('category').prefetch_related('participants')
        participants = ""
        categorys = ""
        groups = ""
    elif type=='totalGroups':
        title = "total groups"
        groups = Group.objects.all()
        events = ""
        participants = ""
        categorys = ""

    totalParticipants = User.objects.filter(rsvp_events__isnull=False).distinct().count()
    # totalParticipants = User.objects.all().count()
    totalCategorys = Category.objects.distinct().count()
    totalEvents = Event.objects.distinct().count()
    upComingEvents = Event.objects.filter(date__gt=date.today()).count()
    pastEvents = Event.objects.filter(date__lt=date.today()).count()
    totalGroups = Group.objects.all().count()

    context = {
        "totalParticipants":totalParticipants,
        "totalCategorys":totalCategorys,
        "totalEvents":totalEvents,
        "upComingEvents":upComingEvents,
        "pastEvents":pastEvents,
        "totalGroups":totalGroups,
        "title":title,
        "events":events,
        "participants":participants,
        "categorys":categorys,
        "groups":groups,
        "user_group_name":user_group_name
        
    }

    return render(request, 'dashboard.html', context)


@login_required
@permission_required('events.delete_event', login_url='no-permission')
def delete_event(request, id):
    
    if request.method=='POST':

        event = Event.objects.get(id=id)
        event.delete()

        messages.success(request, "Successfully event deleted.")
        return redirect('dashboard')
    
    else:
        messages.error(request, "Something went wrong!!")
        return redirect('dashboard')
    

@login_required
@permission_required('events.delete_category', login_url='no-permission')
def delete_category(request, id):

    if request.method=='POST':

        category = Category.objects.get(id=id)
        category.delete()

        messages.success(request, "Category delete done.")
        return redirect('dashboard')
        
    else:
        messages.error(request, "Something went wrong!!")
        return redirect('dashboard')
    

@login_required
@user_passes_test(is_admin, login_url='no-permission')
def delete_participant(request, id):

    if request.method=='POST':

        participant = User.objects.get(id=id)
        participant.delete()

        messages.success(request, "Participant Delete Done.")
        return redirect('dashboard')
    
    else:
        messages.error(request, "Something went wrong!!")
        return redirect('dashboard')
    

@login_required
@permission_required('events.change_event', login_url='no-permission')
def update_event(request,id):
    
    event = Event.objects.get(id=id)

    form = EventModelForm(instance=event)

    if request.method == 'POST':
        form = EventModelForm(request.POST, instance=event)
        
        if form.is_valid():
            form.save()

            messages.success(request, "Successfully Event Updated.")
            return redirect('dashboard')

    return render(request, 'create_event.html', {'form':form})


@login_required
@permission_required('events.change_category')
def update_category(request, id):
    
    category = Category.objects.get(id=id)

    form = CategoryModelForm(instance=category)

    if request.method == 'POST':
        form = CategoryModelForm(request.POST, instance=category)
        
        if form.is_valid():
            form.save()

            messages.success(request, "Successfully Category Updated.")
            return redirect('dashboard')


    return render(request, 'create_category.html', {'form':form})


@login_required
@user_passes_test(is_admin, login_url='no-permission')
def update_participant(request, id):
    
    participant = User.objects.get(id=id)

    form = CustomSignUpModelForm(instance=participant)

    if request.method == 'POST':
        form = CustomSignUpModelForm(request.POST, instance=participant)
        
        if form.is_valid():
            form.save()

            messages.success(request, "Successfully Participant Updated.")
            return redirect('create-participant')


    return render(request, 'create_participant.html', {'form':form})


@login_required(login_url='sign-in')
def details(request, id):
    event = Event.objects.get(id=id)

    return render(request, 'details.html', {'event':event})


@login_required
@user_passes_test(is_admin, login_url='no-permission')
def delete_group(request, id):

    if request.method == "POST":
        group = Group.objects.get(id=id)
        group.delete()

        messages.success(request, "Successfully Group Delete!!")
        return redirect('dashboard')
        
    else:
        messages.error(request, "Something went wrong! Please try again...")
        return redirect('dashboard')




# # user authentication
'''
def signUp(request):
    form = CustomSignUpModelForm()

    if request.method == 'POST':
        form = CustomSignUpModelForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) # create user model object
            user.set_password(form.cleaned_data.get('password1'))
            user.is_active = False
            user.save()
            return redirect('sign-in')

    return render(request, 'signUp.html', {'form':form})

'''

class SignUp(View):

    def get(self, request, *args, **kargs):
        form = CustomSignUpModelForm()
        return render(request, 'signUp.html', {'form':form})
    
    def post(self, request, *args, **kargs):
        form = CustomSignUpModelForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False) # create user model object
            user.set_password(form.cleaned_data.get('password1'))
            user.is_active = False
            user.save()
            messages.success(request, 'Send mail please check your inbox.')
            return redirect('sign-in')

        else:
            messages.error(request, 'Form is not valid!. Please try again...')
            return render(request, 'signUp.html', {'form':form})
'''
def signIn(request):
    form = SignInForm()

    if request.method == 'POST':
        form = SignInForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')

    return render(request, 'signIn.html', {'form':form})

'''

class SignIn(LoginView):
    form_class = SignInForm
    template_name = 'signIn.html'

    def get_success_url(self):
        return reverse_lazy('home')


'''
def signOut(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    
'''

@method_decorator(login_required, name='dispatch')
class SignOut(LogoutView):
    next_page = 'sign-in'

    
@login_required
@user_passes_test(is_admin, login_url='no-permission')
def change_role(request, id):
    user = User.objects.get(id=id)

    form = ChangeRoleForm()
    if request.method == "POST":
        form = ChangeRoleForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data.get('Role')
            role = Group.objects.get(name=data)
            user.groups.clear()
            user.groups.add(role)

            messages.success(request, f"Successfully role change to {user.first_name} {user.last_name}")
            
            return redirect('dashboard')


    return render(request, 'change_role_form.html', {'form':form})


def no_permission(request):
    return render(request, 'no_permission.html')


def rsvp_system(request, id):
    event = Event.objects.get(id=id)
    user = request.user
    event_exist = user.rsvp_events.filter(id=id).exists()

    if event_exist:
        messages.error(request, "You have already rsvp this Event")
        return redirect('home')
    else:
        event.participants.add(user)
        messages.success(request, "Successfully rsvp done. Please check your email")
        return redirect('home')


def activate_user(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):

            user.is_active = True
            user.save()
            
            return redirect('sign-in')
        
    except User.DoesNotExist:
        return HttpResponse("User not found!!!!!!1")
    

class Profile(TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['image'] = user.profile_image
        context['name'] = f'{user.first_name} {user.last_name}'
        context['username'] = user.username
        context['email'] = user.email
        context['member_since'] = user.date_joined
        context['bio'] = user.bio
        context['last_login'] = user.last_login
        context['user_group'] = user.groups.first()

        return context
    

class EditProfile(UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = 'accounts/edit_profile.html'
    context_object_name = 'form'

    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        form.save()
        return redirect('profile')
    


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/password_change.html'
    form_class = CustomPasswordChangeForm


class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'accounts/password_change_done.html'


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/reset_email.html'
    success_url = reverse_lazy('sign-in')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['protocol'] = 'https' if self.request.is_secure() else 'http'
        context['domain'] = self.request.get_host()
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'A Reset email sent. Please check your email.')
        return super().form_valid(form)
        



class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset.html'
    form_class = CustomPasswordResetConfirmForm
    success_url = reverse_lazy('sign-in')

    def form_valid(self, form):
        messages.success(self.request, 'Password Reset Successfully.')
        return super().form_valid(form)