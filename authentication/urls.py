from django.urls import path
from . import views


app_name = 'authentication'


urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.CustomTokenObtainPairView.as_view(), name='login'),
    path('refresh/', views.CustomTokenRefreshView.as_view(), name='refresh'),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    path('activate/', views.activate, name='activate'),
    path('resend-activation/', views.resend_activation, name='resend-activation'),
    path('forgot-password/', views.forgot_password, name='forgot-password'),
    path('reset-password/', views.reset_password, name='reset-password'),
    path('change-password/', views.change_password, name='change-password'),
    path('profile/', views.profile, name='profile')

]