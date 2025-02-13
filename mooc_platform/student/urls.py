from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('profile/', views.profile_update, name='profile'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/<int:course_id>/enroll/', views.student_enrollment, name='student_enrollment'),
    path('courses/<int:course_id>/detail/', views.course_detail, name='course_detail'),
    path('courses/<int:course_id>/review/', views.leave_review, name='leave_review'),
    path('courses/<int:course_id>/enroll/', views.enroll_course, name='enroll_course'),
    path('logout/', views.logout_view, name='logout'),  # Logout URL
    path('courses/<int:course_id>/content/', views.course_content, name='course_content'),
     path('mark_as_completed/<int:content_id>/', views.mark_as_completed, name='mark_as_completed'),
]
