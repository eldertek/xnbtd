# Generated by Django 4.2.6 on 2023-10-24 15:37

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("tours", "0004_remove_chronopostdelivery_breaks_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="breaktime",
            options={
                "verbose_name": "Break Time",
                "verbose_name_plural": "Break Times",
            },
        ),
    ]
