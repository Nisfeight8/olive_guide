from django.urls import path, include
from django.conf.urls import url
from .views import *

app_name = 'user_profile'

urlpatterns = [
    path('', UserUpdateView.as_view(), name='profile'),
    path('password_change', ChangePasswordView.as_view(), name='password_change'),
]