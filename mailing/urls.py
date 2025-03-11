from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import HomePageView, ClientListView, ClientCreateView, ClientDetailView, ClientDeleteView, \
    ClientUpdateView, MessageListView, MessageCreateView, MessageUpdateView, MessageDetailView, MessageDeleteView, \
    MailingListView, MailingCreateView, MailingUpdateView, MailingDetailView, MailingDeleteView, MailingAttemptListView

app_name = MailingConfig.name

urlpatterns = [
path('', HomePageView.as_view(), name='home_page'),
path('clients/', ClientListView.as_view(), name='client_list_page'),
path('clients/create', ClientCreateView.as_view(), name='client_create_page'),
path('clients/update/<int:pk>', ClientUpdateView.as_view(), name='client_update_page'),
path('clients/detail/<int:pk>', ClientDetailView.as_view(), name='client_detail_page'),
path('clients/delete/<int:pk>', ClientDeleteView.as_view(), name='client_delete_page'),

path('messages/', MessageListView.as_view(), name='message_list_page'),
path('messages/create', MessageCreateView.as_view(), name='message_create_page'),
path('messages/update/<int:pk>', MessageUpdateView.as_view(), name='message_update_page'),
path('messages/detail/<int:pk>', MessageDetailView.as_view(), name='message_detail_page'),
path('messages/delete/<int:pk>', MessageDeleteView.as_view(), name='message_delete_page'),

path('mailings/', MailingListView.as_view(), name='mailing_list_page'),
path('mailings/create', MailingCreateView.as_view(), name='mailing_create_page'),
path('mailings/update/<int:pk>', MailingUpdateView.as_view(), name='mailing_update_page'),
path('mailings/detail/<int:pk>', MailingDetailView.as_view(), name='mailing_detail_page'),
path('mailings/delete/<int:pk>', MailingDeleteView.as_view(), name='mailing_delete_page'),

path('attempts/', MailingAttemptListView.as_view(), name='mailing_attempt_list_page'),
]
