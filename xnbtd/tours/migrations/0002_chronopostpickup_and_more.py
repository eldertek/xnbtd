# Generated by Django 4.1.10 on 2023-07-24 15:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tours", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ChronopostPickup",
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
                ("name", models.CharField(max_length=255, verbose_name="Tour Name")),
                ("date", models.DateField(verbose_name="Tour Date")),
                ("esd", models.IntegerField(verbose_name="ESD")),
                ("picked_points", models.IntegerField(verbose_name="Picked Points")),
                ("poste", models.IntegerField(verbose_name="Poste")),
                ("breaks", models.TimeField(verbose_name="Breaks")),
                ("beginning_hour", models.TimeField(verbose_name="Beginning Hour")),
                ("ending_hour", models.TimeField(verbose_name="Ending Hour")),
                (
                    "total_hour",
                    models.FloatField(blank=True, null=True, verbose_name="Total Hour"),
                ),
            ],
            options={
                "verbose_name": "ChronopostPickup",
                "verbose_name_plural": "ChronopostPickup",
            },
        ),
        migrations.RenameModel(
            old_name="Chronopost",
            new_name="ChronopostDelivery",
        ),
        migrations.AlterModelOptions(
            name="chronopostdelivery",
            options={
                "verbose_name": "ChronopostDelivery",
                "verbose_name_plural": "ChronopostDelivery",
            },
        ),
    ]