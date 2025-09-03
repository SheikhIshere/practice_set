from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('edit-profile/', views.edit_profile_view, name='edit_profile'),

    # OTP
    path('verify-email/', views.verify_email_view, name='verify_email'),
    path('verify-login-otp/', views.verify_login_otp_view, name='verify_login_otp'),
    path('resend-otp/', views.resend_otp_view, name='resend_otp'),
]
