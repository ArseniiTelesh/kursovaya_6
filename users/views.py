import secrets

from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView

from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm
from users.models import User


class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token=token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}'
        send_mail(
            subject='Подтверждение почты',
            message=f'Доброго времени суток, перейдите по ссылке для подтверждения почты: {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email, ],
        )
        return super().form_valid(form)


def email_verification (request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:verification_success'))

def verification_success(request):
    """
    Страница-заглушка для более четкого понимания действий пользователем
    """
    return render(request, 'users/verification_success.html')


class UserDetailView(DetailView):
    """Класс для вывода профиля пользователя"""

    model = User

    def get_object(self, queryset=None):
        return self.request.user