from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.utils.crypto import get_random_string
from django.views.generic import CreateView, UpdateView

from users.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from users.models import User
from users.services import send_verify_email


class UserLoginView(LoginView):
    model = User
    form_class = UserLoginForm
    template_name = 'users/login.html'


class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:send_verify')

    def form_valid(self, form):
        if form.is_valid():
            new_user = form.save()
            new_user.verify_token = get_random_string(length=20)
            new_user.save()
            send_verify_email(new_user)
        return super().form_valid(form)


class UserProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('catalog:product_list')

    def get_object(self, queryset=None):
        return self.request.user


def verify(request, verify_key):
    user_item = get_object_or_404(User, verify_token=verify_key)
    user_item.is_active = True
    user_item.verify_token = None
    user_item.save()
    return redirect(reverse('users:verify_success'))


def verify_success(request):
    context = {
        'verifying_message': 'Электронная почта подтверждена.'
    }
    return render(request, 'users/verify_message.html', context)


def send_verify(request):
    context = {
        'verifying_message': 'На вашу электронную почту отправлена ссылка для подтверждения.'
    }
    return render(request, 'users/verify_message.html', context)
