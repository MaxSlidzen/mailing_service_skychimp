from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, DetailView, DeleteView, UpdateView

from mailing.forms import ClientForm
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
