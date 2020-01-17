# Generated by Django 2.2.6 on 2020-01-16 23:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ufdl-core', '0002_the_rest'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('dataset_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ufdl-core.Dataset')),
                ('categories', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='ufdl-core.File', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('ufdl-core.dataset', models.Model),
        ),
    ]