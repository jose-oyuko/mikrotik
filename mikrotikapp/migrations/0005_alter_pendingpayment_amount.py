# Generated by Django 5.1.7 on 2025-04-23 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mikrotikapp", "0004_remove_packages_period_in_hours_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pendingpayment",
            name="amount",
            field=models.IntegerField(),
        ),
    ]
