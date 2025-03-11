from django.urls import reverse_lazy, reverse

from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView

from mailing.forms import ClientForm, MessageForm, MailingForm
from mailing.models import Client, Message, Mailing, MailingAttempt


class HomePageView(TemplateView):
    """
    Домашняя страница
    """
    template_name = 'mailing/home_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_mailings'] = Mailing.objects.count()
        context['active_mailings'] = Mailing.objects.filter(status='created').count()
        context['active_clients'] = Client.objects.filter(mailing__status='created').distinct().count()
        return context


#############      Клиенты      #############
class ClientListView(ListView):
    model = Client


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'mailing/client_form.html'
    success_url = reverse_lazy('mailing:client_list_page')


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'mailing/client_form.html'
    success_url = reverse_lazy('mailing:client_list_page')

class ClientDetailView(DetailView):
    model = Client


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:client_list_page')


##################################################################################

#############      Сообщения      #############

class MessageListView(ListView):
    model = Message


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:message_list_page')


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:message_list_page')


class MessageDetailView(DetailView):
    model = Message


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:message_list_page')


##################################################################################

#############      Рассылки      #############

class MailingListView(ListView):
    model = Mailing


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailing_list_page')


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailing_list_page')


class MailingDetailView(DetailView):
    model = Mailing


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list_page')


##################################################################################

#############      Попытки рассылки (статистика)      #############

class MailingAttemptListView(ListView):
    model = MailingAttempt

