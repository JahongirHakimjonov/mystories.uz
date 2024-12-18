# Generated by Django 5.0.8 on 2024-12-18 07:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("mystories", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="notification",
            name="type",
            field=models.CharField(
                choices=[("SINGLE", "Single"), ("ALL", "All")],
                default="SINGLE",
                max_length=10,
                verbose_name="Type",
            ),
        ),
    ]
