from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg

# Instructor Profile Model
class InstructorProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='instructorprofile')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    bio = models.CharField(max_length=200)
    profile_picture = models.ImageField(upload_to='profile_pics/instructor/', blank=True, null=True, default='images/default.png')

    def __str__(self):
        return f'{self.user.first_name} Profile'
    
# Course Model
class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)
    
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            return reviews.aggregate(Avg('rating'))['rating__avg']
        return None

    def __str__(self):
        return self.title


# Course Content Model (for videos, assignments, etc.)
class CourseContent(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='content')
    content_type = models.CharField(max_length=50)  # e.g., Video, Assignment, Quiz
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='course_content/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)  # For video content
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

# Enrollment Model (Students enrolled in courses)
class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='student_courses')
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='instructor_enrollments')
    course_instructor = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='instructor_courses')

    def __str__(self):
        return f"{self.student} enrolled in {self.course}"

# Course Review Model
class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review for {self.course.title} by {self.student.username}'
