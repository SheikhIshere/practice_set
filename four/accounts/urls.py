from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
    # Auth
    path('signup/', UserRegistrationView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),

    # Profile
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile_edit'),
    path('profile/<slug:username>/', UserProfileView.as_view(), name='profile'),
]
