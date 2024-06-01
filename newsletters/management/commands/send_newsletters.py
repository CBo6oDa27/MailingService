# runapscheduler.py
import logging
import smtplib
from datetime import datetime, timedelta

import pytz
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.db.models import F
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from newsletters.models import Newsletter, SendingHistory

logger = logging.getLogger(__name__)


def newsletters_sender():
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


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            newsletters_sender,
            trigger=CronTrigger(second="*/10"),  # Every 10 seconds
            id="newsletters_sender",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'newsletters_sender'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Начало выполнения регламентного задания...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Остановка планировщика задач...")
            scheduler.shutdown()
            logger.info("Успешное выключение планировщика заданий!")
