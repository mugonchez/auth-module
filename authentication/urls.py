from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView, 
    TokenRefreshView
)

app_name = 'authentication'


urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('activate/', views.activate, name='activate', )
]