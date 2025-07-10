from django.shortcuts import render, redirect
from django.http import HttpResponse
from events.forms import EventModelForm, CategoryModelForm, ParticipantModelForm
from events.models import Event, Category, Participant
from django.contrib import messages
from datetime import date
from django.db.models import Q, Count



# Create your views here.

def search(request):
    base_query = Event.objects.prefetch_related('category').prefetch_related('participants')

    query = request.GET.get('q')

    if query:
        events = base_query.filter(name__icontains=query)

        return render(request, 'search.html', {'events':events})
    
    else:
        return redirect('home')

def home(request):
    events = Event.objects.prefetch_related('category').prefetch_related('participants').filter(date=date.today())
   
    return render(request, 'home.html', {'events':events})


def create_event(request):

    form = EventModelForm()

    if request.method == 'POST':
        form = EventModelForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()

            messages.success(request, "Successfully event created")
            return redirect('dashboard')
 
    return render(request, 'create_event.html', {'form':form})



def create_category(request):

    form = CategoryModelForm()
    
    if request.method == 'POST':
        form = CategoryModelForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(request, "Successfully category created")
            return redirect('dashboard')

    return render(request, 'create_category.html', {'form':form})



def create_participant(request):

    form = ParticipantModelForm()

    if request.method == 'POST':
        form = ParticipantModelForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(request, "Successfully participant created")
            return redirect('dashboard')
        

    return render(request, 'create_participant.html', {'form':form})


def view_event(request):
    
    events = Event.objects.prefetch_related('category').prefetch_related('participants')

    query = request.GET.get('q')
    if query:
        categorys = Category.objects.filter(name__icontains=query)
        if categorys:
            category = categorys.first()
            events = Event.objects.prefetch_related('category').prefetch_related('participants').filter(category=category)
        else:
            messages.error(request, "No category matching!!")
            return redirect('view-event')
    
    startDate = request.GET.get('a')
    endDate = request.GET.get('b')

    if startDate and endDate:    
        events = Event.objects.prefetch_related('category').prefetch_related('participants').filter(date__gte=startDate).filter(date__lte=endDate)
        

    return render(request, 'view_event.html', {'events':events})


def dashboard(request):

    # base_query = Event.objects.prefetch_related('category').prefetch_related('participants')

    type = request.GET.get('type','all')
    if type=='totalParticipant':
        title = "T O T A L    P A R T I C I P A N T ' S"
        participants = Participant.objects.filter(event__isnull=False).distinct()
        events = ""
        categorys = ""
    elif type=='totalCategory':
        title = "T O T A L    C A T E G O R Y ' S"
        categorys = Category.objects.all()
        events = ""
        participants = ""
    elif type=='upcomingEvent':
        title = "U P C O M I N G    E V E N T ' S"
        events = Event.objects.prefetch_related('category').prefetch_related('participants').filter(date__gt=date.today())
        participants = ""
        categorys = ""
    elif type=='pastEvent':
        title = "P A S T    E V E N T ' S"
        events = Event.objects.prefetch_related('category').prefetch_related('participants').filter(date__lt=date.today())
        participants = ""
        categorys = ""
    elif type=='all':
        title = "A L L    E V E N T ' S"
        events = Event.objects.prefetch_related('category').prefetch_related('participants')
        participants = ""
        categorys = ""

    totalParticipant = Participant.objects.filter(event__isnull=False).distinct().count()
    totalCategory = Category.objects.count()
    totalEvent = Event.objects.count()
    upcomingEvent = Event.objects.filter(date__gt=date.today()).count()
    pastEvent = Event.objects.filter(date__lt=date.today()).count()

    context = {
        "totalParticipant":totalParticipant,
        "totalCategory":totalCategory,
        "totalEvent":totalEvent,
        "upcomingEvent":upcomingEvent,
        "pastEvent":pastEvent,
        "title":title,
        "events":events,
        "participants":participants,
        "categorys":categorys
    }

    return render(request, 'dashboard.html', context)



def view_category(request):

    categorys = Category.objects.all()

    return render(request, 'view_category.html', {'categorys':categorys})


def view_participant(request):

    participants = Participant.objects.prefetch_related('event').all()

    return render(request, 'view_participant.html', {'participants':participants})


def delete_event(request, id):
    
    if request.method=='POST':

        event = Event.objects.get(id=id)
        event.delete()

        messages.success(request, "Successfully event deleted.")
        return redirect('dashboard')
    
    else:
        messages.error(request, "Something went wrong!!")
        return redirect('dashboard')
    

def delete_category(request, id):

    if request.method=='POST':

        category = Category.objects.get(id=id)
        category.delete()

        messages.success(request, "Successfully category deleted.")
        return redirect('dashboard')
    
    else:
        messages.error(request, "Category was not delete, something went wrong!!")
        return redirect('dashboard')
    

def delete_participant(request, id):

    if request.method=='POST':

        participant = Participant.objects.get(id=id)
        participant.delete()

        messages.success(request, "Successfully participant deleted.")
        return redirect('dashboard')
    
    else:
        messages.error(request, "Participant was not delete, something went wrong!!")
        return redirect('dashboard')
    


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


def update_participant(request, id):
    
    participant = Participant.objects.get(id=id)

    form = ParticipantModelForm(instance=participant)

    if request.method == 'POST':
        form = ParticipantModelForm(request.POST, instance=participant)
        
        if form.is_valid():
            form.save()

            messages.success(request, "Successfully Participant Updated.")
            return redirect('dashboard')

    return render(request, 'create_participant.html', {'form':form})



def details(request, id):

    event = Event.objects.get(id=id)

    return render(request, 'details.html', {'event':event})