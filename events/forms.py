from django import forms
from events.models import Event, Participant, Category

class EventModelForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'

        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-1/2 px-4 py-2 border rounded-lg mt-2',
           
            }),
            'time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'w-1/2 px-4 py-2 border rounded-lg mt-2'
            }),
            'name': forms.TextInput(attrs={
                'class': 'w-1/2 mt-10 px-4 py-2 border rounded-lg',
                'placeholder': 'Type event name',
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-1/2 mt-2 px-4 py-2 border rounded-lg',
                'placeholder': 'Type event description',
                'rows': 5
            }),
            'location': forms.TextInput(attrs={
                'class': 'w-1/2 px-4 py-2 border rounded-lg mt-2',
                'placeholder': 'Type event location'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'w-1/2 border px-4 py-2 mt-2'
            }),
            'category': forms.Select(attrs={
                'class':'w-1/2 px-4 py-2 border rounded-lg mt-2'
            })
        }



class CategoryModelForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

        widgets = {
                'name': forms.TextInput(attrs={
                    'class': 'w-1/2 mt-10 px-4 py-2 rounded-lg border',
                    'placeholder': 'Type category name'
                }),
                'description': forms.Textarea(attrs={
                    'class': 'w-1/2 mt-2 rounded-lg border',
                    'placeholder': 'Type category description',
                    'rows': 5
                })
            }

class ParticipantModelForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = '__all__'

        widgets = {
            'event': forms.CheckboxSelectMultiple(),
            'name': forms.TextInput(attrs={
                'class': 'w-1/2 px-4 py-2 border mt-10 rounded-lg',
                'placeholder':'Type participant name'
            }),
            'email': forms.TextInput(attrs={
                'class': 'w-1/2 px-4 py-2 border mt-2 rounded-lg',
                'placeholder': 'example@gmail.com'
            })
        }