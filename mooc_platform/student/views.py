from django.shortcuts import render, get_object_or_404, redirect
from .models import Enrollment, CourseProgress, CourseContent
from instructor.models import Course, Review
from .forms import studentForm
import os
from django.contrib.auth import logout
from django.db.models import Avg
from django.contrib import messages


def student_dashboard(request):
    enrolled_courses = Enrollment.objects.filter(student=request.user)
    enrolled_courses_list = [enrollment.course for enrollment in enrolled_courses]
    
    available_courses = Course.objects.exclude(id__in=[course.id for course in enrolled_courses_list])
    
    featured_courses = Course.objects.filter(is_featured=True)
    
    avg_ratings = {}
    for course in enrolled_courses_list:
        avg_ratings[course.id] = Review.objects.filter(course=course).aggregate(Avg('rating'))['rating__avg']
    
    stats = {
        'total_courses': len(enrolled_courses_list),
        'average_rating': sum(rating for rating in avg_ratings.values() if rating is not None) / len(avg_ratings) if avg_ratings else 0
    }

    return render(request, 'student/student_dashboard.html', {
        'enrolled_courses': enrolled_courses_list,
        'available_courses': available_courses,
        'featured_courses': featured_courses,
        'stats': stats
    })


def logout_view(request):
    logout(request)
    return redirect('login')


def profile_update(request):
    if request.method == 'POST':
        form = studentForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            if not profile.profile_picture:
                profile.profile_picture = os.path.join('images/default.png')
            profile.save()
            return redirect('student_dashboard')
    else:
        form = studentForm(instance=request.user.studentprofile)
    return render(request, 'student/profile.html', {'form': form})


def course_list(request):
    courses = Course.objects.all()
    return render(request, 'student/course_list.html', {'courses': courses})


def enroll_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    
    # Prevent the student from enrolling twice in the same course
    if not Enrollment.objects.filter(student=request.user, course=course).exists():
        Enrollment.objects.create(student=request.user, course=course)
        messages.success(request, "You have successfully enrolled in the course!")
    
    # Redirect the user to the course content page after enrollment
    return redirect('course_content', course_id=course.id)

def course_content(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    # Check if the student is enrolled
    if not Enrollment.objects.filter(student=request.user, course=course).exists():
        return redirect('course_list')  # Or you can show a message prompting to enroll

    # Get all content for the course
    course_content = course.content.all()

    # Track the student progress (fetch only relevant progress records)
    student_progress = CourseProgress.objects.filter(student=request.user, course=course)

    # Create a progress dictionary from the progress records
    progress_dict = {content.id: content.is_completed for content in student_progress}

    # Create an empty progress tracker for content if not already created
    if not student_progress.exists():
        for content in course_content:
            if isinstance(content, CourseContent):  # Make sure content is of the right type
                CourseProgress.objects.create(student=request.user, course=course, content=content)

    # Calculate completed and total content
    total_content = course_content.count()
    completed_content = sum(1 for content in course_content if progress_dict.get(content.id, False))

    # Calculate completion percentage
    if total_content > 0:
        completion_percentage = (completed_content / total_content) * 100
    else:
        completion_percentage = 0

    # Get all reviews for the course
    reviews = Review.objects.filter(course=course)

    # Return the context to the template
    return render(request, 'student/course_content.html', {
        'course': course,
        'content': course_content,
        'progress_dict': progress_dict,
        'reviews': reviews,
        'completion_percentage': completion_percentage,  # Pass to template
    })



def course_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    # Check if the student is enrolled
    if not Enrollment.objects.filter(student=request.user, course=course).exists():
        return redirect('course_list')  # Or you can show a message prompting to enroll
    
    # Proceed with displaying course content if enrolled
    return render(request, 'student/course_detail.html', {
        'course': course,
        'reviews': course.reviews.all(),  # Display all reviews related to the course
    })


def student_enrollment(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    
    if not Enrollment.objects.filter(student=request.user, course=course).exists():
        Enrollment.objects.create(student=request.user, course=course)
        messages.success(request, "Successfully enrolled in the course!")
        return redirect('course_content', course_id=course.id)
    
    return redirect('course_content', course_id=course.id)


def leave_review(request, course_id):
    if request.method == 'POST':
        course = get_object_or_404(Course, pk=course_id)
        rating = int(request.POST.get('rating'))
        comment = request.POST.get('comment')
        
        # Prevent multiple reviews from the same student
        if Review.objects.filter(course=course, student=request.user).exists():
            messages.warning(request, "You have already reviewed this course.")
            return redirect('course_content', course_id=course.id)
        
        # Create the review
        Review.objects.create(course=course, student=request.user, rating=rating, comment=comment)
        messages.success(request, "Your review has been submitted successfully.")
    
    return redirect('course_content', course_id=course_id)

def mark_as_completed(request, content_id):
    content = get_object_or_404(CourseContent, pk=content_id)
    progress, created = CourseProgress.objects.get_or_create(student=request.user, course=content.course, content=content)
    
    # Mark content as completed
    if not progress.is_completed:
        progress.is_completed = True
        progress.save()
    
    return redirect('course_content', course_id=content.course.id)