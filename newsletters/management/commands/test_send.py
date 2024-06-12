import smtplib
from datetime import datetime, timedelta

import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.mail import send_mail
from django.core.management import BaseCommand
from django.db.models import F

from config import settings
from newsletters.models import Newsletter, SendingHistory


class Command(BaseCommand):

    def handle(self, *args, **options):
        zone = pytz.timezone(settings.TIME_ZONE)
        current_datetime = datetime.now(zone)
        # Получим рассылки в статусе "Создана" и "Запущена" для обработки.
        newsletters_queue = Newsletter.objects.filter(status__in=["Создана", "Запущена"])
        for newsletter in newsletters_queue:
            if (
                    newsletter.mail_active
                    and newsletter.start_date <= current_datetime
                    and newsletter.mail_datetime <= current_datetime
                    and newsletter.status == "Создана"
            ):
                try:
                    send_mail(
                        subject=newsletter.message.title,
                        message=newsletter.message.content,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[client.email for client in newsletter.client.all()],
                    )
                    newsletter.mail_status = "Запущена"
                    newsletter.save()
                    if (
                            newsletter.periodicity == "Раз в день"
                            and (current_datetime - newsletter.start_date).days >= 1
                    ):
                        newsletter.mail_datetime = F("mail_datetime") + timedelta(days=1)
                        newsletter.save()
                    elif (
                            newsletter.periodicity == "Раз в неделю"
                            and (current_datetime - newsletter.start_date).days >= 7
                    ):
                        newsletter.mail_datetime = F("mail_datetime") + timedelta(days=7)
                        newsletter.save()
                    elif (
                            newsletter.periodicity == "Раз в месяц"
                            and (current_datetime - newsletter.start_date).days >= 30
                    ):
                        newsletter.mail_datetime = F("mail_datetime") + timedelta(days=30)
                        newsletter.save()
                    attempt = SendingHistory.objects.create(
                        datetime=current_datetime,
                        status="Успешно",
                        settings=newsletter,
                    )
                    attempt.save()
                except smtplib.SMTPResponseException as error:
                    attempt = SendingHistory.objects.create(
                        datetime=current_datetime,
                        status="Были ошибки",
                        response=str(error),
                        settings=newsletter,
                    )
                    attempt.save()
