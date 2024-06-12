from django.db import models

from users.models import User

NULLABLE = {"null": True, "blank": True}


class Client(models.Model):
    """Клиент сервиса, для получения рассылки"""

    name = models.CharField(
        max_length=100, verbose_name="Ф.И.О", help_text="Введите ФИО получателя"
    )
    email = models.EmailField(
        verbose_name="Контактный email", help_text="Введите адрес электронной почты"
    )
    comment = models.TextField(
        verbose_name="Комментарий", **NULLABLE, help_text="Введите комментарий"
    )

    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Владелец", **NULLABLE
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

        permissions = [
            ('block_the_user', 'Can block the user'),
            ('view_all_users', 'Can view all users'),
        ]


class Message(models.Model):
    """Сообщение для рассылки"""

    title = models.CharField(
        max_length=100, verbose_name="Тема письма", help_text="Введите тему письма"
    )
    content = models.TextField(
        verbose_name="Содержание", help_text="Введите содержимое письма"
    )

    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Владелец", **NULLABLE
    )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"


class Newsletter(models.Model):
    """Рассылка по клиентам с настройками расписания"""

    PeriodicityOfSending = [
        ("Раз в день", "Раз в день"),
        ("Раз в неделю", "Раз в неделю"),
        ("Раз в месяц", "Раз в месяц"),
    ]

    StatusesOfSending = [
        ("Создана", "Создана"),
        ("Запущена", "Запущена"),
        ("Завершена", "Завершена"),
    ]
    title = models.CharField(
        max_length=100, verbose_name="Тема", help_text="Введите тему рассылки"
    )
    mail_datetime = models.DateTimeField(
        verbose_name="Начало отправки рассылки", **NULLABLE
    )
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, verbose_name="Сообщение"
    )
    client = models.ManyToManyField(
        Client, verbose_name="Клиент", related_name="client"
    )
    start_date = models.DateTimeField(
        verbose_name="Дата и время первой отправки рассылки", **NULLABLE
    )
    periodicity = models.CharField(
        verbose_name="Периодичность",
        choices=PeriodicityOfSending,
        help_text="Выберите частоту отправки",
    )
    status = models.CharField(
        verbose_name="Статус отправки",
        choices=StatusesOfSending,
        default=StatusesOfSending[0][0],
    )
    mail_active = models.BooleanField(verbose_name="Активность рассылки", default=True)

    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Владелец", **NULLABLE
    )

    def __str__(self):
        return f"{self.title} ({self.status})"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"

        permissions = [
            ('can_manage_newsletter_status', 'Can manage newsletter status')
        ]


class SendingHistory(models.Model):
    """Попытка рассылки - история отправки рассылок"""

    Statuses = [
        ("success", "Успешно"),
        ("fail", "Ошибка"),
    ]
    datetime = models.DateTimeField(
        verbose_name="Дата и время попытки", auto_now_add=True
    )
    status = models.CharField(max_length=50, choices=Statuses, verbose_name="Cтатус")
    response = models.CharField(verbose_name="Ответ почтового сервера", **NULLABLE)
    settings = models.ForeignKey(
        Newsletter, verbose_name="Настройка рассылки", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.settings}, {self.datetime}, {self.status}"

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылки"
