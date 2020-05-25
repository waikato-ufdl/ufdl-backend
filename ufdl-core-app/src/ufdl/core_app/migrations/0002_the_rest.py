# Generated by Django 2.2.6 on 2020-05-25 22:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import ufdl.core_app.models._User


class Migration(migrations.Migration):

    dependencies = [
        ('simple_django_teams', '0002_rename_organisations_to_teams'),
        ('ufdl-core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Condition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('deletion_time', models.DateTimeField(default=None, editable=False, null=True)),
                ('is_public', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=200)),
                ('version', models.IntegerField(default=1)),
                ('description', models.TextField()),
                ('tags', models.TextField()),
                ('unstructured', models.TextField()),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
                'default_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('handle', models.CharField(max_length=128)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
                'default_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='Filename',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(editable=False, max_length=200)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
                'default_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='Licence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Limitation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='NamedFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
                'default_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', ufdl.core_app.models._User.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('deletion_time', models.DateTimeField(default=None, editable=False, null=True)),
                ('name', models.CharField(max_length=200)),
                ('creator', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='projects', to='simple_django_teams.Team')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
                'default_manager_name': 'objects',
            },
        ),
        migrations.AddConstraint(
            model_name='permission',
            constraint=models.UniqueConstraint(fields=('name',), name='unique_permission_names'),
        ),
        migrations.AddField(
            model_name='namedfile',
            name='file',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='ufdl-core.File'),
        ),
        migrations.AddField(
            model_name='namedfile',
            name='name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='ufdl-core.Filename'),
        ),
        migrations.AddConstraint(
            model_name='limitation',
            constraint=models.UniqueConstraint(fields=('name',), name='unique_limitation_names'),
        ),
        migrations.AddField(
            model_name='licence',
            name='conditions',
            field=models.ManyToManyField(related_name='_licence_conditions_+', to='ufdl-core.Condition'),
        ),
        migrations.AddField(
            model_name='licence',
            name='limitations',
            field=models.ManyToManyField(related_name='_licence_limitations_+', to='ufdl-core.Limitation'),
        ),
        migrations.AddField(
            model_name='licence',
            name='permissions',
            field=models.ManyToManyField(related_name='_licence_permissions_+', to='ufdl-core.Permission'),
        ),
        migrations.AddConstraint(
            model_name='filename',
            constraint=models.UniqueConstraint(fields=('filename',), name='unique_filenames'),
        ),
        migrations.AddConstraint(
            model_name='file',
            constraint=models.UniqueConstraint(fields=('handle',), name='unique_file_handles'),
        ),
        migrations.AddField(
            model_name='dataset',
            name='creator',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='dataset',
            name='files',
            field=models.ManyToManyField(related_name='_dataset_files_+', to='ufdl-core.NamedFile'),
        ),
        migrations.AddField(
            model_name='dataset',
            name='licence',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='datasets', to='ufdl-core.Licence'),
        ),
        migrations.AddField(
            model_name='dataset',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='datasets', to='ufdl-core.Project'),
        ),
        migrations.AddConstraint(
            model_name='condition',
            constraint=models.UniqueConstraint(fields=('name',), name='unique_condition_names'),
        ),
        migrations.AddConstraint(
            model_name='project',
            constraint=models.UniqueConstraint(condition=models.Q(deletion_time__isnull=True), fields=('name', 'team'), name='unique_active_project_names_per_team'),
        ),
        migrations.AddConstraint(
            model_name='namedfile',
            constraint=models.UniqueConstraint(fields=('name', 'file'), name='unique_filename_file_pairs'),
        ),
        migrations.AddConstraint(
            model_name='licence',
            constraint=models.UniqueConstraint(fields=('name',), name='unique_licence_names'),
        ),
        migrations.AddConstraint(
            model_name='dataset',
            constraint=models.UniqueConstraint(fields=('name', 'version', 'project'), name='unique_datasets_per_project'),
        ),
    ]
