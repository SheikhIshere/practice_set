from django.urls import path
from .views import UserRegisterView, UserLoginView, UserLogoutView, ProfileView

app_name = 'account'

urlpatterns = [    
    path('signup/', UserRegisterView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),

]