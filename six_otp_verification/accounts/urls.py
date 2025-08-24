from django.urls import path
from .views import *
app_name = 'accounts'

urlpatterns = [        
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('profile/', ProfileVeiw.as_view(), name='profile'),    
]
