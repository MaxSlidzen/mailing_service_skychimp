from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import HomeView

app_name = MailingConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]
