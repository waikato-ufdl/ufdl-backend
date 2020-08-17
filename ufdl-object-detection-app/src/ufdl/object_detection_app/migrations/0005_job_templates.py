from django.db import migrations

from ufdl.core_app.migrations.job_templates import get_python_job_template_migration

from .job_templates import iterate_job_templates


class Migration(migrations.Migration):
    """
    Migration inserting the pre-trained model presets into the database.
    """
    dependencies = [
        ('ufdl-object-detection', '0004_pretrained_models')
    ]

    operations = [
        migrations.RunPython(get_python_job_template_migration(iterate_job_templates()))
    ]
