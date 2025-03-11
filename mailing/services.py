from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from apscheduler.schedulers.background import BackgroundScheduler

from mailing.models import Mailing, MailingAttempt

def send_mailing():
    now = timezone.now()
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
            mailing.last_sent = now
            mailing.save()
            continue

        # Периодическая рассылка
        last_attempt = MailingAttempt.objects.filter(mailing=mailing).order_by('-datetime_last_mailing').first()

        if mailing.frequency == 'daily' and last_attempt and (now - last_attempt.datetime_last_mailing).days < 1:
            continue
        if mailing.frequency == 'weekly' and last_attempt and (now - last_attempt.datetime_last_mailing).days < 7:
            continue
        if mailing.frequency == 'monthly' and last_attempt and (now - last_attempt.datetime_last_mailing).days < 30:
            continue
        if mailing.end_datetime and now > mailing.end_datetime:
            mailing.status = 'completed'
            mailing.save()
            continue

        if mailing.status == 'created':
            mailing.status = 'activated'
            mailing.save()

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