from django.db import migrations


def add_groups_and_permissions(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    group_data = [
        {"name": "GLS", "permissions": [24, 5, 8]},
        {"name": "TNT - Fedex", "permissions": [24, 13, 16]},
        {"name": "Ciblex", "permissions": [24, 17, 20]},
        {"name": "Chronopost", "permissions": [24, 9, 12]}
    ]

    for data in group_data:
        group = Group.objects.create(name=data['name'])
        permissions = Permission.objects.filter(pk__in=data['permissions'])
        group.permissions.set(permissions)


class Migration(migrations.Migration):

    dependencies = []

    operations = [
        migrations.RunPython(add_groups_and_permissions),
    ]
