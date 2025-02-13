from django.urls import path
from .views import registration, CustomLogin, logout_view

urlpatterns = [
  path('register/', registration , name='register'),
  path('login/', CustomLogin.as_view(), name='login'),
  path('logout/', logout_view, name='logout')
  
]