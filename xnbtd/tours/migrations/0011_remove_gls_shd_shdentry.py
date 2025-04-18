# Generated by Django 4.2.6 on 2025-01-04 16:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("tours", "0010_alter_gls_packages_refused"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="gls",
            name="shd",
        ),
        migrations.CreateModel(
            name="SHDEntry",
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
                ("number", models.PositiveIntegerField(verbose_name="SHD Number")),
                ("value", models.IntegerField(verbose_name="Value")),
                (
                    "gls",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="shd_entries",
                        to="tours.gls",
                        verbose_name="GLS Tour",
                    ),
                ),
            ],
            options={
                "verbose_name": "SHD Entry",
                "verbose_name_plural": "SHD Entries",
                "ordering": ["number"],
                "unique_together": {("gls", "number")},
            },
        ),
    ]
