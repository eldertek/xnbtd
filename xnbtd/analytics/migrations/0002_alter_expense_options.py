# Generated by Django 4.2.6 on 2025-04-25 22:41

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("analytics", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="expense",
            options={
                "ordering": ["-date"],
                "permissions": [
                    (
                        "view_financial_data",
                        "Can view financial data and pricing information",
                    )
                ],
                "verbose_name": "Dépense",
                "verbose_name_plural": "Dépenses",
            },
        ),
    ]
