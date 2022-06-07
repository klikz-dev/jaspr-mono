from django.db import migrations


def do_nothing(apps, schema_editor):
    """ We are doing nothing here so that we can have fake a migration on production and maintain 0006 on integration"""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("clinics", "0005_custom_slugify_names_for_organization_code"),
    ]

    operations = [
        migrations.RunPython(
            do_nothing,
            reverse_code=migrations.RunPython.noop,
            elidable=True,
        )
    ]
