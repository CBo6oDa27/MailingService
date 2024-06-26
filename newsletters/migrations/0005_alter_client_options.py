# Generated by Django 4.2.2 on 2024-06-12 13:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("newsletters", "0004_alter_newsletter_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="client",
            options={
                "permissions": [
                    ("block_the_user", "Can block the user"),
                    ("view_all_users", "Can view all users"),
                ],
                "verbose_name": "Клиент",
                "verbose_name_plural": "Клиенты",
            },
        ),
    ]
