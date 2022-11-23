# Generated by Django 2.2.13 on 2021-03-01 00:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ufdl_core', '0002_the_rest'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageClassificationDataset',
            fields=[
                ('dataset_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ufdl_core.Dataset')),
            ],
            options={
                'abstract': False,
            },
            bases=('ufdl_core.dataset',),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.TextField()),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='categories', to='ufdl_core.FileReference')),
            ],
        ),
        migrations.AddConstraint(
            model_name='category',
            constraint=models.UniqueConstraint(fields=('file', 'category'), name='unique_categories_for_file'),
        ),
    ]
