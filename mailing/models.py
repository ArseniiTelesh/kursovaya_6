from django.db import models
from django.utils.timezone import now

NULLABLE = {"null": True, "blank": True}

PERIODICITY_CHOICES = [
    ('once', 'Однократно'),
    ('daily', 'Раз в день'),
    ('weekly', 'Раз в неделю'),
    ('monthly', 'Раз в месяц'),
    ('yearly', 'Раз в год'),
]

STATUS_MAILING = [
    ('created', 'Создана'),
    ('activated', 'Запущена'),
    ('completed', 'Завершена'),
]


class Client(models.Model):
    """
    Модель клиента (принимающего рассылки)
    """
    name = models.CharField(max_length=300, verbose_name='Имя клиента')
    email = models.EmailField(max_length=100, verbose_name='Почта клиента')
    comment = models.TextField(verbose_name='сообщение', **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name='активен')

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f"{self.email}"



class Message(models.Model):
    """
    Модель сообщения (что рассылается при помощи рассылки)
    """
    title = models.CharField(max_length=300, verbose_name='Тема сообщения')
    body = models.TextField(verbose_name='Текст сообщения')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return f"Тема письма: {self.title}"


class Mailing(models.Model):
    """
    Модель рассылки
    """
    message = models.ForeignKey(Message, on_delete=models.CASCADE, **NULLABLE, verbose_name='Сообщение')
    client = models.ManyToManyField(Client, verbose_name='Клиент')

    name = models.CharField(max_length=30,default='Рассылка № ', verbose_name='название рассылки')
    datetime_first_mailing = models.DateTimeField(default=now, verbose_name='Дата и время начала рассылки')
    end_datetime = models.DateTimeField(verbose_name='Дата и время окончания рассылки', **NULLABLE)
    frequency = models.CharField(max_length=150, verbose_name='Периодичность рассылки', choices=PERIODICITY_CHOICES, default='once')
    status = models.CharField(max_length=150, verbose_name='Статус рассылки', choices=STATUS_MAILING, default='created')
    last_sent = models.DateTimeField(verbose_name='Последняя отправка', **NULLABLE)

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class MailingAttempt(models.Model):
    """
    Модель попытки рассылки (лог)
    """
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='текст рассылки')

    datetime_last_mailing = models.DateTimeField(verbose_name='Дата и время последней отправки рассылки')
    status_attempt = models.BooleanField(verbose_name='Статус', default=False)
    server_answer = models.CharField(verbose_name='ответ почтового сервера', **NULLABLE)

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылки'
