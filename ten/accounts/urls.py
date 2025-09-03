from django.urls import path
from .views import SignupView, UserLoginView, ProfileView
from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView

app_name = 'accounts'

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('accounts:login')), name='logout'),
    path('profile/<slug:username>', ProfileView.as_view(), name='profile')
]