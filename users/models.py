from django.db import models

class User(models.Model):
    """
    Модель пользователя (создающего рассылки)
    """
    name = models.CharField(max_length=150, verbose_name='Имя пользователя')
    email = models.EmailField(max_length=200, verbose_name='Электронная почта')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f"{self.name}, ({self.email})"