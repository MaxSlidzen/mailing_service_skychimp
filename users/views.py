from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.utils.crypto import get_random_string
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView

from mailing.models import Mailing
from users.forms import UserLoginForm, UserRegisterForm, UserUpdateForm
from users.models import User
from users.services import send_verify_email, get_cache_user


class UserLoginView(UserPassesTestMixin, LoginView):
    model = User
    form_class = UserLoginForm
    template_name = 'users/login.html'
    extra_context = {
        'title': 'Вход на портал'
    }

    def test_func(self):
        return not self.request.user.is_authenticated


class UserRegisterView(UserPassesTestMixin, CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:send_verify')
    extra_context = {
        'title': 'Регистрация'
    }

    def test_func(self):
        return not self.request.user.is_authenticated

    def form_valid(self, form):
        if form.is_valid():
            new_user = form.save()
            new_user.verify_token = get_random_string(length=20)
            new_user.save()
            send_verify_email(new_user)
        return super().form_valid(form)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    success_url = reverse_lazy('mailing:home')
    extra_context = {
        'title': 'Мой профиль'
    }

    def get_object(self, queryset=None):
        return self.request.user


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    extra_context = {
        'title': 'Удаление аккаунта'
    }
    success_url = reverse_lazy('mailing:home')

    def test_func(self):
        return self.request.user.pk == self.get_object().pk or self.request.user.is_superuser


class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    extra_context = {
        'title': 'Список пользователей'
    }

    def test_func(self):
        user = self.request.user
        return (user.is_staff and not user.has_perm('blog.add_article')) or user.is_superuser


class UserDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = User
    extra_context = {
        'title': 'Пользователь'
    }

    def test_func(self):
        user = self.request.user
        return (user.is_staff and not user.has_perm('blog.add_article')) or user.is_superuser

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        # Если убрать строку, вместо текущего пользователя (в меню) будет отображаться выбранный
        context_data['user'] = self.request.user

        context_data['mailings'] = get_cache_user(self.get_object())
        return context_data


@user_passes_test(lambda u: (u.is_staff and not u.has_perm('blog.add_article')) or u.is_superuser)
@login_required
def toggle_activity(request, pk):
    user_item = get_object_or_404(User, pk=pk)
    if user_item.is_active:
        user_item.is_active = False
    else:
        user_item.is_active = True

    user_item.save()

    return redirect(reverse('users:user_detail', args=[user_item.pk]))


def verify(request, verify_key):
    user_item = get_object_or_404(User, verify_token=verify_key)
    user_item.is_active = True

    # Удаление значения токена для снижения вероятности ошибки уникальности при создании токена для нового пользователя
    user_item.verify_token = None
    user_item.save()
    context = {
        'title': 'Подтверждение регистрации',
        'verifying_message': 'Электронная почта подтверждена.'
    }
    return render(request, 'users/verify_message.html', context)


def send_verify(request):
    context = {
        'title': 'Подтверждение регистрации',
        'verifying_message': 'На вашу электронную почту отправлена ссылка для подтверждения.'
    }
    return render(request, 'users/verify_message.html', context)
