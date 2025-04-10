# Generated by Django 5.1.7 on 2025-04-02 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mikrotikapp", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="PayedTransaction",
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
                ("transaction_id", models.CharField(max_length=36, unique=True)),
                ("reference", models.CharField(max_length=20)),
                ("origination_time", models.DateTimeField()),
                ("sender_phone_number", models.CharField(max_length=15)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("till_number", models.CharField(max_length=10)),
                (
                    "sender_first_name",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "sender_middle_name",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "sender_last_name",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ["-origination_time"],
            },
        ),
        migrations.DeleteModel(
            name="PayedTransactions",
        ),
    ]
