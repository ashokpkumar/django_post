# Generated by Django 5.0.6 on 2024-06-06 12:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("post_man", "0002_usermodel_delete_user"),
    ]

    operations = [
        migrations.CreateModel(
            name="OrderModel",
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
                ("order_id", models.CharField(max_length=50, unique=True)),
                ("location", models.CharField(max_length=100)),
                ("street_address", models.CharField(max_length=100)),
                ("landmark", models.CharField(max_length=100)),
                ("priority", models.IntegerField()),
                ("phone_number", models.CharField(max_length=20)),
                ("door_number", models.CharField(max_length=20)),
                ("order_weight", models.DecimalField(decimal_places=2, max_digits=5)),
                (
                    "order_status",
                    models.CharField(
                        choices=[
                            ("delivered", "Delivered"),
                            ("damaged", "Damaged"),
                            ("customer_not_reachable", "Customer Not Reachable"),
                            ("customer_rejects", "Customer Rejects"),
                        ],
                        max_length=100,
                    ),
                ),
            ],
        ),
    ]
