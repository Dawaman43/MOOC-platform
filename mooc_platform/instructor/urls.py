from django.urls import path
from .views import instructor_dashboard, profile_update, profile_view, courses, course_content, enrolled_students

urlpatterns = [
    path('instructor/', instructor_dashboard, name='instructor_dashboard'),
    path('instructor/profile/', profile_update, name='profile'),
    path('instructor/profile_view/', profile_view, name='profile_view'),
    path('instructor/course/', courses, name='course'),
    # Fix the URL pattern to accept a course ID
    path('instructor/course_detail/<int:course_id>/', course_content, name='instructor_course_detail'),
    path('instructor/enrolled-students/', enrolled_students, name='enrolled_students'),
]
