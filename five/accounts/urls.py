from django.urls import path
from .views import (
    SignUpView, 
    UserLoginView as LoginView, 
    UserLogoutView as LogoutView,
    ProfileView,
    ProfileEditView,
    ProfileRedirectView,
)

app_name = 'accounts'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<slug:username>/', ProfileView.as_view(), name='profile'),
    path('profile_edit/', ProfileEditView.as_view(), name='profile_edit'),
    path('profile_redirect/', ProfileRedirectView.as_view(), name='profile_redirect'),
]
