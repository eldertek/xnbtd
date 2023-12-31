# Generated by Django 4.1.10 on 2023-07-21 21:35

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Event",
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
                ("date", models.DateField(verbose_name="Date")),
                ("title", models.CharField(max_length=100, verbose_name="Title")),
            ],
            options={
                "verbose_name": "Event",
                "verbose_name_plural": "Events",
                "ordering": ["date"],
            },
        ),
    ]
