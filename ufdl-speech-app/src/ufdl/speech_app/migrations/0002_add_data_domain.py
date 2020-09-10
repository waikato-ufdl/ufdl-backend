from django.db import migrations

from ufdl.core_app.migrations import add_data_domain, DataMigration


class Migration(migrations.Migration):
    """
    Migration adding this data domain to the database.
    """
    dependencies = [
        ('ufdl-core', '0002_the_rest'),
        ('ufdl-speech', '0001_initial')
    ]

    operations = [
        DataMigration(add_data_domain('sp', "Speech"))
    ]
