from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('refresh/', views.refresh_token, name='refresh')
]