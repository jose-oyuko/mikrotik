# Generated by Django 5.1.7 on 2025-06-20 03:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mikrotikapp", "0011_alter_sessions_mac_address"),
    ]

    operations = [
        migrations.AddField(
            model_name="sessions",
            name="mpesa_code",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name="tickets",
            name="ticketPassword",
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name="tickets",
            name="ticketUsername",
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
