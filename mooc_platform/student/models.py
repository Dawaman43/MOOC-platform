from django.db import models
from django.contrib.auth.models import User
from instructor.models import Course, Review

class studentModel(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  first_name = models.CharField(max_length=50)
  last_name = models.CharField(max_length=50, null=True)
  profile_picture = models.ImageField(upload_to='profile_pics/student/', blank=True, null=True, default='images/default.png')

  def __str__(self):
    return f'{self.user.first_name}'

class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="enrollments")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="students")
    enrolled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.student.first_name} enrolled in {self.course.title}'


class CourseContent(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    content_type = models.CharField(max_length=100, choices=[('video', 'Video'), ('document', 'Document')])

    def __str__(self):
        return self.title
    
class CourseProgress(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.ForeignKey(CourseContent, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.student.username} - {self.course.title} - {self.content.title}'
