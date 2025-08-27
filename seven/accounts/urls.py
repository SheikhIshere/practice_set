from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('profile/<str:username>/', UserProfileView.as_view(), name='profile'),
]
