from django.urls import  path
from django.contrib.auth.views import LogoutView
from .views  import *

app_name = 'accounts'

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', SigninView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='accounts:login'), name='logout'),
    path('profile_update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),
]


