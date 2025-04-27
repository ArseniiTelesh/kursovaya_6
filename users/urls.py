from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import UserRegisterView, email_verification, verification_success, UserDetailView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path("email-confirm/<str:token>", email_verification, name='email_verification'),
    path('verification_success/', verification_success, name='verification_success'),
    path('profile_detail/', UserDetailView.as_view(), name='profile_detail'),
]
