from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import HomeView, ClientCreateView, ClientDeleteView, ClientDetailView, ClientListView, \
    ClientUpdateView, MailingDeleteView, MailingUpdateView, MailingListView, MailingCreateView, MailingDetailView, \
    MailingLogListView, toggle_status

app_name = MailingConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('client_list/', ClientListView.as_view(), name='client_list'),
    path('client_detail_<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('client_create/', ClientCreateView.as_view(), name='client_create'),
    path('client_update_<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('client_delete_<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),

    path('mailing_list_<int:pk>/', MailingListView.as_view(), name='mailing_list'),
    path('mailing_detail_<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailing_create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailing_update_<int:pk>/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailing_delete_<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),

    path('toggle_status_<int:pk>/', toggle_status, name='toggle_status'),

    path('log_list_<int:pk>/', MailingLogListView.as_view(), name='log_list'),
]
