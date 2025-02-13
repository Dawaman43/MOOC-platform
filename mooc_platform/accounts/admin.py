from django.contrib import admin
from django.contrib.auth.models import User
from .models import Profile

class UserAdmin(admin.ModelAdmin):
  list_display = (
    'username', 'first_name', 'last_name', 'email', 'is_staff', 'get_role'
  )
  search_fields = (
    'username','first_name', 'last_name', 'email'
  )
  list_filter = (
    'is_staff', 'is_superuser', 'groups'
  )
  filter_horizontal = (
    'groups', 'user_permissions'
  )


  def get_role(self, obj):
    return obj.profile.role if hasattr(obj, 'profile') else 'No role'
  get_role.short_description = 'Role'
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class ProfileAdmin(admin.ModelAdmin):
  list_display = (
    'user' , 'role'
  )

  search_fields = (
    'user__username', 'role'
  )
  list_filter= (
    'role',
  )
admin.site.register(Profile, ProfileAdmin)


# class courseAdmin(admin.ModelAdmin):
#   list_display = (
#     'user' , 'cour'
#   )