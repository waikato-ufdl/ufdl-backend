from django.db import migrations

from ufdl.core_app.migrations import DataMigration
from ufdl.core_app.migrations import add_data_domain


class Migration(migrations.Migration):
    """
    Migration adding this data domain to the database.
    """
    dependencies = [
        ('ufdl_core', '0002_the_rest'),
        ('ufdl_spectrum_classification', '0001_initial')
    ]

    operations = [
        DataMigration(add_data_domain('sc', "Spectrum Classification"))
    ]
