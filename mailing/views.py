import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, CreateView, ListView, DetailView, DeleteView, UpdateView

from mailing.forms import ClientForm, MailingForm
from mailing.models import Client, Mailing, MailingLog
from users.models import User


class HomeView(TemplateView):
    template_name = 'mailing/home.html'
    extra_context = {
        'title': 'Главная'
    }

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['myself'] = self.request.user


class ClientListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Client
    extra_context = {
        'title': 'Мой список клиентов'
    }

    def test_func(self):
        return self.request.user.is_superuser or not self.request.user.is_staff

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(added_by_id=self.request.user.id)

        return queryset


class ClientDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Client
    extra_context = {
        'title': 'Просмотр клиента'
    }

    def test_func(self):
        return self.request.user == self.get_object().added_by

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['mailings'] = Mailing.objects.filter(client=self.object)
        return context_data


class ClientCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')
    extra_context = {
        'title': 'Добавление клиента'
    }

    def test_func(self):
        return not self.request.user.is_staff or self.request.user.is_superuser

    def form_valid(self, form):
        if form.is_valid():
            new_client = form.save()
            new_client.added_by = self.request.user
            new_client.save()

        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')
    extra_context = {
        'title': 'Редактирование клиента'
    }

    def test_func(self):
        return self.request.user == self.get_object().added_by


class ClientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:client_list')
    extra_context = {
        'title': 'Удаление клиента'
    }

    def test_func(self):
        return self.request.user == self.get_object().added_by


class MailingListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Mailing
    extra_context = {
        'title': 'Рассылки'
    }

    def test_func(self):
        if self.kwargs.get('pk') != 0:
            author = User.objects.get(pk=self.kwargs.get('pk'))
            return self.request.user.is_staff or self.request.user == author
        else:
            return self.request.user.is_staff

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.kwargs.get('pk') != 0:
            if self.request.user.is_staff and not self.request.user.is_superuser:
                raise Http404('Отсутствуют права доступа')
            queryset = queryset.filter(author=self.request.user.id)
        else:
            if not self.request.user.is_staff:
                raise Http404('Отсутствуют права доступа')

        return queryset

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        print(type(self.kwargs.get('pk')))
        if self.kwargs.get('pk') == 0:
            context_data['all_mailings'] = True
            context_data['title'] = 'Все рассылки'
        else:
            context_data['title'] = 'Мои рассылки'

        return context_data


class MailingDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Mailing
    extra_context = {
        'title': 'Просмотр рассылки'
    }

    def test_func(self):
        return self.request.user.is_staff or self.request.user == self.get_object().author

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['clients'] = Client.objects.filter(mailing=self.object)
        context_data['logs'] = MailingLog.objects.filter(mailing=self.object).order_by('-pk')[
                               :len(context_data['clients'])]
        return context_data


class MailingCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    extra_context = {
        'title': 'Добавление рассылки'
    }
    permission_required = 'mailing.add_mailing'

    def test_func(self):
        return not self.request.user.is_staff or self.request.user.is_superuser

    def get_success_url(self):
        return reverse('mailing:mailing_list', args=[self.request.user.id])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        if form.is_valid():
            new_mailing = form.save()
            new_mailing.author = self.request.user
            new_mailing.save()

        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    extra_context = {
        'title': 'Редактирование рассылки'
    }

    def test_func(self):
        return self.request.user == self.get_object().author or self.request.user.is_superuser

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse('mailing:mailing_list', args=[self.request.user.id])


class MailingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')
    extra_context = {
        'title': 'Удаление рассылки'
    }

    def test_func(self):
        return self.request.user == self.get_object().author or self.request.user.is_superuser

    def get_success_url(self):
        return reverse('mailing:mailing_list', args=[self.request.user.id])


class MailingLogListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = MailingLog
    extra_context = {
        'title': 'Логи'
    }

    def test_func(self):
        author = Mailing.objects.get(pk=self.kwargs.get('pk')).author
        return self.request.user == author or self.request.user.is_superuser

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(mailing=self.kwargs.get('pk'))

        return queryset


@login_required
def toggle_status(request, pk):
    mailing_item = get_object_or_404(Mailing, pk=pk)

    if request.user != mailing_item.author and not request.user.is_staff:
        raise Http404('Отсутствуют права доступа')

    mailing_start_datetime = datetime.datetime.combine(mailing_item.start_date, mailing_item.time)
    if mailing_item.stop_date is not None and mailing_item.stop_date <= datetime.date.today():
        raise Http404('Невозможно активировать завершенную рассылку. Измените дату завершения')
    elif mailing_item.status in ['started', 'created']:
        mailing_item.status = 'done'
    else:
        if mailing_start_datetime < datetime.datetime.now():
            mailing_item.status = 'started'
        else:
            mailing_item.status = 'created'

    mailing_item.save()

    return redirect(reverse('mailing:mailing_detail', args=[pk]))
