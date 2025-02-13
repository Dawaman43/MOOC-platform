from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from instructor.models import InstructorProfile



class userCreation(UserCreationForm):
  first_name = forms.CharField(max_length=50, required=True, 
                               widget=forms.TextInput(attrs={"class" : "form-control", "placeholder" : "JOE"}))
  last_name = forms.CharField(max_length=50, required=True, 
                              widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'DOE'}))
  email = forms.EmailField(required=True, 
                           widget=forms.EmailInput(attrs={'class' : 'form-control', 'placeholder' : '123@example.com'}))
  password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'form-control'}))
  password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'form-control'}))
  role = forms.ChoiceField(choices=[('student','student'), ('instructor', 'instructor')])
  class Meta:
    model = get_user_model()
    fields = ['first_name','last_name', 'email','username', 'password1', 'password2']
    widgets = {
      'username' : forms.TextInput(attrs={'class' : 'form-control'}),
    }
  
  def save(self, commit=True):
    user = super().save(commit=False)
    if commit:
        user.save()

        # Create the instructor profile only if the role is 'instructor'
        if self.cleaned_data['role'] == 'instructor':
            InstructorProfile.objects.create(
                user=user,  # Ensure the user_id is set correctly
                first_name=user.first_name,
                last_name=user.last_name,
                bio='',  # Default bio or empty string
                profile_picture=None  # Default or None
            )
    
    return user
