# Generated by Django 4.1.7 on 2023-03-18 20:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("margin_check", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="basemarginreport",
            name="margin",
            field=models.DecimalField(
                decimal_places=1, max_digits=6, verbose_name="margin"
            ),
        ),
    ]
