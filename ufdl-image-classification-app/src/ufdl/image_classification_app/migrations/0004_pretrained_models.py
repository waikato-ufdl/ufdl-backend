from django.db import migrations

from ufdl.core_app.migrations import DataMigration
from ufdl.core_app.migrations.pretrained_models import get_python_pretrained_model_migration

from .pretrained_models import iterate_pretrained_models


class Migration(migrations.Migration):
    """
    Migration inserting the pre-trained model presets into the database.
    """
    dependencies = [
        ('ufdl-image-classification', '0003_docker')
    ]

    operations = [
        DataMigration(get_python_pretrained_model_migration(iterate_pretrained_models()))
    ]
