from django import forms
from events.models import Event, Participant, Category

class EventModelForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'

        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }



class CategoryModelForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'



class ParticipantModelForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = '__all__'

        widgets = {
            'event': forms.CheckboxSelectMultiple()
        }