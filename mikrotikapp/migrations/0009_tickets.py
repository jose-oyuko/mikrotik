# Generated by Django 5.1.7 on 2025-05-20 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mikrotikapp", "0008_commands"),
    ]

    operations = [
        migrations.CreateModel(
            name="Tickets",
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
                ("ticketUsername", models.CharField(max_length=100)),
                ("ticketPassword", models.CharField(max_length=100)),
                ("ticketPeriod", models.CharField(max_length=100)),
                ("used", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
