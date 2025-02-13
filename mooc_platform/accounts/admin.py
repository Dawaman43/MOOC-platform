from django.contrib import admin
from instructor.models import InstructorProfile, Course, CourseContent, Enrollment, Review
from django.db.models import Avg


# Instructor Profile Admin
class InstructorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'bio', 'profile_picture')
    search_fields = ('user__username', 'first_name', 'last_name')
    list_filter = ('user__is_staff',)
    readonly_fields = ('user',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


# Course Admin
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'category', 'price', 'created_at', 'is_featured', 'average_rating_display')
    search_fields = ('title', 'instructor__username', 'category')
    list_filter = ('category', 'is_featured', 'created_at')
    filter_horizontal = ('students',)
    
    def average_rating_display(self, obj):
        avg_rating = obj.average_rating()
        return avg_rating if avg_rating else "No ratings yet"
    average_rating_display.short_description = 'Average Rating'

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('reviews')


# Course Content Admin
class CourseContentAdmin(admin.ModelAdmin):
    list_display = ('course', 'content_type', 'title', 'file', 'video_url', 'description')
    search_fields = ('course__title', 'title', 'content_type')
    list_filter = ('content_type', 'course')


# Enrollment Admin
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'instructor', 'course_instructor')
    search_fields = ('student__username', 'course__title', 'instructor__username')
    list_filter = ('course', 'student', 'instructor')


# Review Admin
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('course', 'student', 'rating', 'created_at', 'comment')
    search_fields = ('course__title', 'student__username', 'rating')
    list_filter = ('rating', 'created_at')


# Registering models with the admin site
admin.site.register(InstructorProfile, InstructorProfileAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(CourseContent, CourseContentAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
admin.site.register(Review, ReviewAdmin)

