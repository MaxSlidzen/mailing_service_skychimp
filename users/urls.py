from django.contrib.auth.views import LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import UserRegisterView, UserProfileView, UserLoginView, verify, verify_success, send_verify

app_name = UsersConfig.name

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('verify_<str:verify_key>/', verify, name='verify'),
    path('verify_success', verify_success, name='verify_success'),
    path('send_verify', send_verify, name='send_verify'),
]
