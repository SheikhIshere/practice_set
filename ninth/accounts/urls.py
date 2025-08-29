from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordChangeDoneView

app_name = 'accounts'

urlpatterns = [
    path('signup/', SignupView.as_view(), name = 'signup'),
    path('login/', UserLoginView.as_view(), name = 'login'),
    path('logout/', LogoutView.as_view(next_page = reverse_lazy('accounts:login')), name = 'logout'),    
    path('profile-update/', ProfileUpdateView.as_view(), name = 'profile_update'),
    path('profile/<slug:username>', ProfileView.as_view(), name = 'profile'),

    # testing password reset
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    # Password change
    path('password-change/', PasswordChangeView.as_view(template_name='password_change.html', success_url=reverse_lazy('accounts:password_change_done')), name='password_change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),

]