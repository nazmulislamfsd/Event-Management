from django.shortcuts import render, redirect
from django.http import HttpResponse
from events.forms import EventModelForm, CategoryModelForm, ParticipantModelForm
from events.models import Event, Category, Participant
from django.contrib import messages



# Create your views here.

def create_event(request):

    if request.method == 'POST':
        form = EventModelForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()

            messages.success(request, "Event Created Successfully")
            return redirect('create-event')
    
    else:
        form = EventModelForm()

    return render(request, 'create_event.html', {'form':form})



def create_category(request):
    
    if request.method == 'POST':
        form = CategoryModelForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(request, "Category Created Done")
            return redirect('create-category')

    else:
        form = CategoryModelForm()

    return render(request, 'create_category.html', {'form':form})



def create_participant(request):

    if request.method == 'POST':
        form = ParticipantModelForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(request, "Participant Created Done")
            return redirect('create-participant')
        
    else:
        form = ParticipantModelForm()
    
    return render(request, 'create_participant.html', {'form':form})


def view_event(request):

    events = Event.objects.select_related('category').all()

    return render(request, 'view_event.html', {'events':events})


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

        messages.success(request, "Event delete done.")
        return redirect('view-event')
    
    else:
        messages.error(request, "Something went wrong!!")
        return redirect('view-event')
    

def delete_category(request, id):

    if request.method=='POST':

        category = Category.objects.get(id=id)
        category.delete()

        messages.success(request, "Category delete done.")
        return redirect('view-category')
    
    else:
        messages.error(request, "Something went wrong!!")
        return redirect('view-category')
    


def delete_participant(request, id):

    if request.method=='POST':

        participant = Participant.objects.get(id=id)
        participant.delete()

        messages.success(request, "participant delete done.")
        return redirect('view-participant')
    
    else:
        messages.error(request, "Something went wrong!!")
        return redirect('view-participant')
    


def update_event(request,id):
    
    event = Event.objects.get(id=id)

    form = EventModelForm(instance=event)

    if request.method == 'POST':
        form = EventModelForm(request.POST, instance=event)
        
        if form.is_valid():
            form.save()

            messages.success(request, "Successfully Event Updated.")
            return redirect('view-event')


    return render(request, 'create_event.html', {'form':form})




def update_category(request, id):
    
    category = Category.objects.get(id=id)

    form = CategoryModelForm(instance=category)

    if request.method == 'POST':
        form = CategoryModelForm(request.POST, instance=category)
        
        if form.is_valid():
            form.save()

            messages.success(request, "Successfully Category Updated.")
            return redirect('view-category')


    return render(request, 'create_category.html', {'form':form})




def update_participant(request, id):
    
    participant = Participant.objects.get(id=id)

    form = ParticipantModelForm(instance=participant)

    if request.method == 'POST':
        form = ParticipantModelForm(request.POST, instance=participant)
        
        if form.is_valid():
            form.save()

            messages.success(request, "Successfully participant Updated.")
            return redirect('view-participant')


    return render(request, 'create_participant.html', {'form':form})




