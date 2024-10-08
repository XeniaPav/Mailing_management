# Generated by Django 4.2.2 on 2024-09-21 12:03

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Attempt",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "start_date",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        verbose_name="Дата и время начала рассылки",
                    ),
                ),
                (
                    "end_date",
                    models.DateTimeField(
                        blank=True,
                        null=True,
                        verbose_name="Дата и время окончания рассылки",
                    ),
                ),
                (
                    "mailing_status",
                    models.BooleanField(
                        default=False, verbose_name="Успешна ли попытка"
                    ),
                ),
                (
                    "server_response",
                    models.TextField(
                        default=False, verbose_name="Ответ почтового сервера"
                    ),
                ),
            ],
            options={
                "verbose_name": "Попытка рассылки",
                "verbose_name_plural": "Попытки рассылки",
            },
        ),
        migrations.CreateModel(
            name="Client",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        help_text="Введите email клиента",
                        max_length=254,
                        unique=True,
                        verbose_name="Email",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Введите имя клиента",
                        max_length=150,
                        verbose_name="Имя клиента",
                    ),
                ),
                (
                    "comment",
                    models.TextField(
                        blank=True,
                        help_text="Введите комментарий к клиенту",
                        null=True,
                        verbose_name="Комментарий",
                    ),
                ),
            ],
            options={
                "verbose_name": "Клиент",
                "verbose_name_plural": "Клиенты",
            },
        ),
        migrations.CreateModel(
            name="Message",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "subject",
                    models.CharField(max_length=100, verbose_name="Тема сообщения"),
                ),
                ("text", models.TextField(verbose_name="Текст сообщения")),
            ],
            options={
                "verbose_name": "Сообщение",
                "verbose_name_plural": "Сообщения",
            },
        ),
        migrations.CreateModel(
            name="Newsletter",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        blank=True,
                        default="Рассылка",
                        max_length=100,
                        null=True,
                        verbose_name="Название рассылки",
                    ),
                ),
                (
                    "start_date",
                    models.DateField(verbose_name="Дата и время первой рассылки"),
                ),
                (
                    "frequency",
                    models.CharField(
                        choices=[
                            ("Ежедневно", "Ежедневно"),
                            ("Еженедельно", "Еженедельно"),
                            ("Ежемесячно", "Ежемесячно"),
                        ],
                        default="Ежедневно",
                        max_length=50,
                        verbose_name="Периодичность",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Создана", "Создана"),
                            ("Запущена", "Запущена"),
                            ("Завершена", "Завершена"),
                        ],
                        default="Создана",
                        max_length=50,
                        verbose_name="Статус рассылки",
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                (
                    "clients",
                    models.ManyToManyField(
                        blank=True,
                        related_name="clients",
                        to="mail.client",
                        verbose_name="Клиенты",
                    ),
                ),
                (
                    "message",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="message",
                        to="mail.message",
                        verbose_name="Сообщение",
                    ),
                ),
            ],
            options={
                "verbose_name": "Рассылка",
                "verbose_name_plural": "Рассылки",
                "permissions": [
                    ("can_block_newsletter", "Can block newsletter"),
                    ("can_view_newsletter", "Can view newsletter"),
                    ("can_view_user", "Can view user"),
                    ("can_block_user", "Can block user"),
                ],
            },
        ),
    ]
