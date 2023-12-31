from django.contrib.auth.views import LogoutView
from django.urls import path
from django.views.decorators.cache import cache_page

from users.apps import UsersConfig
from users.views import UserRegisterView, UserUpdateView, UserLoginView, verify, send_verify, \
    toggle_activity, UserDetailView, UserListView, UserDeleteView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('profile/', UserUpdateView.as_view(), name='profile'),
    path('user_detail_<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('user_delete_<int:pk>/', UserDeleteView.as_view(), name='user_delete'),
    path('verify_<str:verify_key>/', verify, name='verify'),
    path('send_verify/', send_verify, name='send_verify'),
    path('activity/<int:pk>/', toggle_activity, name='toggle_activity'),
    path('user_list/', cache_page(30)(UserListView.as_view()), name='user_list'),

]
