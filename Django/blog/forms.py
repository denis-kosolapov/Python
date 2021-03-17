from django import forms
from .models import Contacts, SenderEmails

class CheckBox(forms.BooleanField):
    field = forms.CheckboxInput()

class ContactForm(forms.ModelForm):
    checkbox = CheckBox()
    class Meta():
        model = Contacts
        fields = ['name', 'email', 'phone', 'description', 'checkbox']