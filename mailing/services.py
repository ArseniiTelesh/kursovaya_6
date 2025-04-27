from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.cache import cache
from config.settings import CACHE_ENABLED

from mailing.models import Mailing, MailingAttempt

def send_mailing():
    """Просматривает все рассылки, проверяет время, если время рассылки, отправляет письма"""

    now = timezone.now()

    if CACHE_ENABLED:
        key = 'mailings'
        mailings = cache.get(key)
        if mailings is None:
            mailings = Mailing.objects.filter(
                datetime_first_mailing__lte=now,
                status='created'
            )
            cache.set(key, mailings, 300)  # Кешируем на 5 минут
    else:
        mailings = Mailing.objects.filter(
            datetime_first_mailing__lte=now,
            status='created'
        )

    for mailing in mailings:
        if mailing.frequency == 'once':
            # Однократная рассылка
            for client in mailing.client.all():
                try:
                    send_mail(
                        subject=mailing.message.title,
                        message=mailing.message.body,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[client.email],
                        fail_silently=False
                    )
                    status = True
                    response = "Sent successfully"
                except Exception as e:
                    status = False
                    response = str(e)

                MailingAttempt.objects.create(
                    mailing=mailing,
                    datetime_last_mailing=now,
                    status_attempt=status,
                    server_answer=response
                )

            mailing.status = 'completed'
            mailing.is_active= False
            mailing.last_sent = now
            mailing.save()
            continue

        # Для периодической рассылки
        last_attempt = MailingAttempt.objects.filter(mailing=mailing).order_by('-datetime_last_mailing').first()

        # Проверка нужно ли отправлять (периодичность)
        need_send = True
        if last_attempt:
            if mailing.frequency == 'daily' and (now - last_attempt.datetime_last_mailing).days < 1:
                need_send = False
            elif mailing.frequency == 'weekly' and (now - last_attempt.datetime_last_mailing).days < 7:
                need_send = False
            elif mailing.frequency == 'monthly' and (now - last_attempt.datetime_last_mailing).days < 30:
                need_send = False

        # Проверка окончания рассылки
        if mailing.end_datetime and now > mailing.end_datetime:
            mailing.status = 'completed'
            mailing.is_active = False
            mailing.save()
            continue

        # Активация новой рассылки
        if mailing.status == 'created':
            mailing.status = 'activated'
            mailing.is_active = True
            mailing.save()

        # Отправка если нужно
        if need_send:
            for client in mailing.client.all():
                try:
                    send_mail(
                        subject=mailing.message.title,
                        message=mailing.message.body,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[client.email],
                        fail_silently=False
                    )
                    status = True
                    response = "Sent successfully"
                except Exception as e:
                    status = False
                    response = str(e)

                MailingAttempt.objects.create(
                    mailing=mailing,
                    datetime_last_mailing=now,
                    status_attempt=status,
                    server_answer=response
                )

            mailing.last_sent = now
            mailing.save()


def start():
    """ Функция для реализации периодических задач """
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_mailing, 'interval', seconds=600)
    scheduler.start()