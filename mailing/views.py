from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, CreateView, ListView, DetailView, DeleteView, UpdateView

from mailing.forms import ClientForm, MailingForm
from mailing.models import Client, Mailing


class HomeView(TemplateView):
    template_name = 'mailing/home.html'
    extra_context = {
        'title': 'Главная'
    }


class ClientListView(ListView):
    model = Client
    extra_context = {
        'title': 'Мой список клиентов'
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(added_by_id=self.request.user.id)

        return queryset


class ClientDetailView(DetailView):
    model = Client
    extra_context = {
        'title': 'Просмотр клиента'
    }

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['mailings'] = Mailing.objects.filter(client=self.object)
        return context_data


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')
    extra_context = {
        'title': 'Добавление клиента'
    }

    def form_valid(self, form):
        if form.is_valid():
            new_client = form.save()
            new_client.added_by = self.request.user
            new_client.save()

        return super().form_valid(form)


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')
    extra_context = {
        'title': 'Редактирование клиента'
    }


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:client_list')
    extra_context = {
        'title': 'Удаление клиента'
    }


class MailingListView(ListView):
    model = Mailing
    extra_context = {
        'title': 'Рассылки'
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.kwargs.get('pk') != 0:
            queryset = queryset.filter(author=self.request.user.id)

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


class MailingDetailView(DetailView):
    model = Mailing
    extra_context = {
        'title': 'Просмотр рассылки'
    }

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['clients'] = Client.objects.filter(mailing=self.object)
        return context_data


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    extra_context = {
        'title': 'Добавление рассылки'
    }

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


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    extra_context = {
        'title': 'Редактирование рассылки'
    }

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse('mailing:mailing_list', args=[self.request.user.id])


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')
    extra_context = {
        'title': 'Удаление рассылки'
    }

    def get_success_url(self):
        return reverse('mailing:mailing_list', args=[self.request.user.id])
