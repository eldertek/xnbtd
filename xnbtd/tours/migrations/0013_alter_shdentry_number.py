# Generated by Django 4.2.6 on 2025-01-04 16:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tours", "0012_alter_breaktime_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="shdentry",
            name="number",
            field=models.PositiveIntegerField(editable=False, verbose_name="SHD"),
        ),
    ]
