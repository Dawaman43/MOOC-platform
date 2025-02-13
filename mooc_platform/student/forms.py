from django import forms
from .models import studentModel

class studentForm(forms.ModelForm):
  class Meta:
    model = studentModel
    fields = [
      'first_name', 'last_name', 'profile_picture'
    ]
    widgets = {
      'first_name' : forms.TextInput(attrs={'class' : 'form-contol'}),
      'last_name' : forms.TextInput(attrs={'class' : 'form-contol'}),
    }