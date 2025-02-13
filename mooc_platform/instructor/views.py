
from django.shortcuts import render, redirect,  get_object_or_404
import os

from .forms import InstructorProfileForm, CoursesForm, CourseFileForm
from django.contrib.auth.decorators import login_required
from .models import Course, Enrollment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, FormView
from django.contrib import messages

@login_required
def instructor_dashboard(request):
    return render(request, 'instructor/instructor_dashboard.html')

@login_required
def profile_update(request):
    # Get the first (or None if no profile exists) instructorProfile for the logged-in user
    profile = request.user.instructorprofile.first()  # Use .first() to get the first profile (or None if not found)

    if request.method == 'POST':
        form = InstructorProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            
            # Assign the logged-in user to the profile
            profile.user = request.user

            request.session['first_name'] = profile.first_name
            
            # Fix this line to correctly use os.path.join
            if not profile.profile_picture:
                profile.profile_picture = os.path.join('images', 'profile_picture')
            
            profile.save()
            return redirect('profile')  # Make sure 'profile' is defined in your URLs
    else:
        form = InstructorProfileForm(instance=profile)

    return render(request, 'instructor/profile.html', {'form': form})

def profile_view(request):
    if request.method == 'POST':
        form = InstructorProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save()
            profiles ={
               ' first_name' : profile.first_name,
                'last_name ': profile.last_name
            }
        return render(request, 'instructor/instructor_dashboard.html', {'profiles': profile})
    else:
        form = InstructorProfileForm()
    return redirect(request, 'instructor/instructor_dashboard.html', {'form':form})
       

@login_required
def courses(request):
    if request.method == 'POST':
        course_form = CoursesForm(request.POST)
        file_form = CourseFileForm(request.POST, request.FILES)

        if course_form.is_valid() and file_form.is_valid():
            course = course_form.save(commit=False)
            course.instructor = request.user  # Assign instructor
            course.save()

            file = file_form.save(commit=False)
            file.course = course  # Link file to course
            file.save()

            messages.success(request, "Course and file uploaded successfully!")
            return redirect('course')  # Redirect to the course dashboard after submission
    else:
        course_form = CoursesForm()
        file_form = CourseFileForm()

    all_courses = Course.objects.filter(instructor=request.user).order_by('-created_at')

    return render(request, 'instructor/course.html', {
        'courses': course_form,
        'files': file_form,
        'all_courses': all_courses
    })

@login_required
def course_content(request, course_id):
    course = Course.objects.get(id=course_id)
    course_content = course.contents.all()  # Check if this is being populated
    course_files = course.files.all()  # Ensure files are being fetched

    # Debugging - print to console
    print(course_content)  # This should show the content related to the course
    print(course_files)    # This should show the files related to the course

    # Progress tracking logic (if applicable)
    progress_dict = {}  # Or actual logic to track progress
    return render(request, 'student/course_content.html', {
        'course': course,
        'course_content': course_content,
        'course_files': course_files,
        'progress_dict': progress_dict,
    })

@login_required
def enrolled_students(request):
    enrollments = Enrollment.objects.select_related('student', 'course').all()  # Optimized query
    return render(request, 'instructor/enrolled_students.html', {'enrollments': enrollments})