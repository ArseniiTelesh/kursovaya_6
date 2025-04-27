from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse

from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView

from blog.models import Blog
from mailing.forms import ClientForm, MessageForm, MailingForm
from mailing.models import Client, Message, Mailing, MailingAttempt


class UserRequiredMixin:  # миксин блокирует доступ пользователя к чужим объектам
    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user

        if (self.object.owner == user  # владелец
            or user.is_superuser       # суперюзер
            or user.groups.filter(name='Менеджер').exists()  # состоит в группе "менеджер"
        ):
            return self.object
        raise Http404


class HomePageView(TemplateView):
    """
    Домашняя страница
    """
    template_name = 'mailing/home_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_mailings'] = Mailing.objects.count()
        context['active_mailings'] = Mailing.objects.filter(
            status='activated',
            is_active=True
        ).count()
        context['active_clients'] = Client.objects.filter(
            mailing__status='activated',
            mailing__is_active=True
        ).distinct().count()

        context['blog'] = Blog.objects.all().order_by('created')[:3]
        return context



#############      Клиенты      #############
class ClientListView(LoginRequiredMixin, ListView):
    model = Client

    def get_queryset(self):
        return super().get_queryset().filter(
            owner=self.request.user
        )

class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'mailing/client_form.html'
    success_url = reverse_lazy('mailing:client_list_page')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UserRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'mailing/client_form.html'
    success_url = reverse_lazy('mailing:client_list_page')

class ClientDetailView(LoginRequiredMixin, UserRequiredMixin, DetailView):
    model = Client


class ClientDeleteView(UserRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:client_list_page')


##################################################################################

#############      Сообщения      #############

class MessageListView(LoginRequiredMixin, ListView):
    model = Message

    def get_queryset(self):
        return super().get_queryset().filter(
            owner=self.request.user
        )


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:message_list_page')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UserRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:message_list_page')


class MessageDetailView(LoginRequiredMixin, UserRequiredMixin, DetailView):
    model = Message


class MessageDeleteView(UserRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:message_list_page')


##################################################################################

#############      Рассылки      #############

class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing

    def get_queryset(self):
        return super().get_queryset().filter(
            owner=self.request.user
        )


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailing_list_page')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UserRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailing_list_page')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    @login_required
    def change_mailing_is_active(request, **kwargs):
        """Управление активностью рассылки"""
        mailing = get_object_or_404(Mailing, id=kwargs['pk'])

        # Проверка прав: владелец или менеджер
        if not (request.user == mailing.owner or
                request.user.groups.filter(name='Менеджер').exists()):
            raise PermissionDenied

        # Логика переключения
        if kwargs['act']:  # Активация
            if mailing.status == 'created' and mailing.datetime_first_mailing <= timezone.now():
                mailing.status = 'activated'
                mailing.is_active = True
        else:  # Деактивация
            mailing.status = 'completed'
            mailing.is_active = False

        mailing.save()
        return redirect(reverse('mailing:mailing_list'))

class MailingDetailView(LoginRequiredMixin, UserRequiredMixin, DetailView):
    model = Mailing


class MailingDeleteView(UserRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list_page')


##################################################################################

#############      Попытки рассылки (статистика)      #############

class MailingAttemptListView(ListView):
    model = MailingAttempt

