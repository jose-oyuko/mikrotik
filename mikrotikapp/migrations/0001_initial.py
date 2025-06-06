# Generated by Django 5.1.7 on 2025-04-13 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Packages",
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
                ("price", models.IntegerField()),
                ("period_in_hours", models.IntegerField()),
            ],
        ),
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
        migrations.CreateModel(
            name="sessions",
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
                ("mac_address", models.CharField(max_length=17)),
                ("package_amount", models.IntegerField()),
                ("starting_time", models.DateTimeField(auto_now_add=True)),
                ("end_time", models.DateTimeField()),
                ("phone_number", models.CharField(max_length=15)),
                ("period", models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name="PendingPayment",
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
                ("phoneNumber", models.CharField(max_length=15)),
                ("macAddress", models.CharField(max_length=17)),
                ("ipAddress", models.GenericIPAddressField()),
                ("payed", models.BooleanField(default=False)),
                ("time", models.DateTimeField(auto_now_add=True)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                "indexes": [
                    models.Index(
                        fields=["phoneNumber", "amount"],
                        name="mikrotikapp_phoneNu_1baccc_idx",
                    )
                ],
            },
        ),
    ]
