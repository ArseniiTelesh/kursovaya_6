from django.urls import path

from mailing.views import index

urlpatterns = [
    path('', index)
]