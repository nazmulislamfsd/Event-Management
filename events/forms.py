from django import forms
from events.models import Event, Category
from django.contrib.auth.models import User, Group
import re
from django.contrib.auth.forms import AuthenticationForm


# StyleFormMixin

class StyledFormMixin:
    """ Mixing to apply style to form field"""

    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.apply_styled_widgets()

    default_classes = "w-1/2 p-3 mt-3 rounded-lg shadow-sm focus:outline-none"

    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder':  f"Enter {field.label.lower()}",
                    'rows': 5
                })
            elif isinstance(field.widget, forms.DateInput):
                field.widget.attrs.update({
                    "class": self.default_classes
                })
            elif isinstance(field.widget, forms.TimeInput):
                field.widget.attrs.update({
                    "class": self.default_classes
                })
            elif isinstance(field.widget, forms.PasswordInput):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class': "space-y-2"
                })
            else:
                field.widget.attrs.update({
                    'class': self.default_classes
                })


# class UserModelForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = '__all__'


class EventModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        
        labels = {
            'name': 'Event Name',
            'description': 'Description',
            'participants': 'Select Participants',
            'date': 'Event Date',
            'time': 'Start Time',
            'location': 'Event Location',
            'image': 'Event Image',
            'category': 'Event Category',
        }

        widgets = {
            'name': forms.TextInput(),
            'description': forms.Textarea(),
            'participants': forms.SelectMultiple,
            'date': forms.DateInput(attrs={'type':'date'}),
            'time': forms.TimeInput(attrs={'type':'time'}),
            'location': forms.TextInput(),
            'image': forms.ClearableFileInput(),
            'category': forms.Select()
        }



class CategoryModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

        labels = {
            'name': 'Category Name',
            'description': 'Category Description',
        }

        widgets = {
                'name': forms.TextInput,
                'description': forms.Textarea
            }
        

class GroupModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Group
        fields = '__all__'

        widgets = {
                'name': forms.TextInput(),
                'permissions': forms.SelectMultiple()
            }


class ChangeRoleForm(StyledFormMixin, forms.Form):
    Role = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        empty_label="Select a Role"
    )


class CustomSignUpModelForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'confirm_password', 'email']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
            
        self.fields['username'].help_text = None

    # field error
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if len(password1)<8:
            raise forms.ValidationError("password must be at least 8 character long")
        elif not re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{8,}', password1):
            raise forms.ValidationError("password must be Character, Number and Special Character (@#$%^&+=) only")
        
        return password1
    
    # non-field error
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        confirm_password = cleaned_data.get('confirm_password')

        if password1 and confirm_password:
            if password1 != confirm_password:
                raise forms.ValidationError("password don't match.")
        else:
            raise forms.ValidationError("please fill-up password1 and confirm_password field")
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_exist = User.objects.filter(email=email).exists()

        if email_exist:
            raise forms.ValidationError("email already exist")
        
        return email
    

class SignInForm(StyledFormMixin, AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

