from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tours", "0014_remove_gls_shd"),
    ]

    operations = [
        # avp_relay est masqué de l'UI mais la colonne et ses données sont conservées
        migrations.AlterField(
            model_name="gls",
            name="avp_relay",
            field=models.IntegerField(
                verbose_name="AVP Relais", null=True, blank=True, editable=False
            ),
        ),
        migrations.AddField(
            model_name="gls",
            name="picked_points",
            field=models.IntegerField(verbose_name="Points ramassés", null=True, blank=True),
        ),
    ]
