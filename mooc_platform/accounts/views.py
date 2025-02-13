from django.shortcuts import render,redirect
from django.urls import reverse

from .models import Profile
from .forms import userCreation
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView

def registration(request):
    if request.method == 'POST':
        form = userCreation(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user object first
            role = form.cleaned_data['role']
            
            # Create Profile associated with the user
            Profile.objects.create(user=user, role=role)  # This ensures that the 'user_id' is not null
            
            login(request, user)  # Log the user in after registration
            
            if role == 'student':
                return redirect('student_dashboard')
            else:
                return redirect('instructor_dashboard')
    else:
        form = userCreation()  # Initialize form for GET request

    return render(request, 'account/register.html', {'form': form})
class CustomLogin(LoginView):
    template_name = 'account/login.html'

    def form_valid(self, form):
        # This method is called when the form is valid (user is authenticated)
        user = form.get_user()
        
        # Proceed with the default login handling
        return super().form_valid(form)

    def get_success_url(self):
        # Get the user from the request
        user = self.request.user

        # Check if the user has a profile and return the corresponding dashboard URL
        if hasattr(user, 'profile'):
            if user.profile.role == 'student':
                return reverse('student_dashboard')  # Use reverse() to get the URL
            elif user.profile.role == 'instructor':
                return reverse('instructor_dashboard')  # Use reverse() to get the URL
        
        # Default redirection if no role is found
        return reverse('home')  # Redirect to home if no role is set

def logout_view(request):
    logout(request)
    return redirect('login')