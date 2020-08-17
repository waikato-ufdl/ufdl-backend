# Generated by Django 2.2.13 on 2020-08-11 22:11

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
            name='CUDAVersion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.DecimalField(decimal_places=1, max_digits=4, unique=True)),
                ('full_version', models.CharField(max_length=16, unique=True)),
                ('min_driver_version', models.CharField(max_length=16)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DataDomain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=2, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('deletion_time', models.DateTimeField(default=None, editable=False, null=True)),
                ('is_public', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=200)),
                ('version', models.IntegerField(default=1, editable=False)),
                ('previous_version', models.IntegerField(default=-1, editable=False)),
                ('description', models.TextField(blank=True)),
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
            name='DockerImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('version', models.CharField(max_length=32)),
                ('url', models.CharField(max_length=200)),
                ('registry_url', models.CharField(max_length=200)),
                ('registry_username', models.CharField(max_length=64, null=True)),
                ('registry_password', models.CharField(max_length=64, null=True)),
                ('cpu', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='DockerImageToJobType',
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
            name='Domain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
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
            name='FileReference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metadata', models.TextField(blank=True, default='')),
            ],
        ),
        migrations.CreateModel(
            name='Framework',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('version', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='Hardware',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('generation', models.CharField(max_length=32)),
                ('min_compute_capability', models.FloatField()),
                ('max_compute_capability', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Input',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('type', models.CharField(max_length=32)),
                ('options', models.TextField(blank=True, default='')),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('deletion_time', models.DateTimeField(default=None, editable=False, null=True)),
                ('start_time', models.DateTimeField(default=None, editable=False, null=True)),
                ('end_time', models.DateTimeField(default=None, editable=False, null=True)),
                ('error', models.TextField(default=None, null=True)),
                ('input_values', models.TextField()),
                ('parameter_values', models.TextField(blank=True)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
                'default_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='JobOutput',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('deletion_time', models.DateTimeField(default=None, editable=False, null=True)),
                ('name', models.CharField(max_length=200)),
                ('type', models.CharField(blank=True, default='', max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='JobTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('deletion_time', models.DateTimeField(default=None, editable=False, null=True)),
                ('name', models.CharField(max_length=64)),
                ('version', models.IntegerField(default=1)),
                ('scope', models.CharField(max_length=16)),
                ('executor_class', models.CharField(max_length=128)),
                ('required_packages', models.TextField(blank=True)),
                ('body', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='JobType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True)),
            ],
            options={
                'abstract': False,
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
            name='LogEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('level', models.PositiveSmallIntegerField()),
                ('is_internal', models.BooleanField(default=False, editable=False)),
                ('message', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('deletion_time', models.DateTimeField(default=None, editable=False, null=True)),
            ],
            options={
                'abstract': False,
            },
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
            name='Node',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=39)),
                ('driver_version', models.CharField(max_length=16)),
                ('gpu_mem', models.PositiveIntegerField()),
                ('cpu_mem', models.PositiveIntegerField()),
                ('last_seen', models.DateTimeField(null=True, default=None)),
            ],
        ),
        migrations.CreateModel(
            name='Parameter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('type', models.CharField(max_length=32)),
                ('default', models.TextField()),
            ],
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
            name='PreTrainedModel',
            fields=[
                ('model_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ufdl-core.Model')),
                ('url', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
            bases=('ufdl-core.model',),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('deletion_time', models.DateTimeField(default=None, editable=False, null=True)),
                ('name', models.CharField(max_length=200)),
                ('creator', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, null=True)),
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
            model_name='parameter',
            name='template',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='parameters', to='ufdl-core.JobTemplate'),
        ),
        migrations.AddField(
            model_name='node',
            name='current_job',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='ufdl-core.Job'),
        ),
        migrations.AddField(
            model_name='node',
            name='hardware_generation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='nodes', to='ufdl-core.Hardware'),
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
        migrations.AddField(
            model_name='model',
            name='creator',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='model',
            name='data',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='ufdl-core.File'),
        ),
        migrations.AddField(
            model_name='model',
            name='domain',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='models', to='ufdl-core.DataDomain'),
        ),
        migrations.AddField(
            model_name='model',
            name='framework',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='models', to='ufdl-core.Framework'),
        ),
        migrations.AddField(
            model_name='model',
            name='licence',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='models', to='ufdl-core.Licence'),
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
            name='domains',
            field=models.ManyToManyField(related_name='_licence_domains_+', to='ufdl-core.Domain'),
        ),
        migrations.AddField(
            model_name='user',
            name='node',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user', to='ufdl-core.Node', null=True, default=None),
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
        migrations.AddField(
            model_name='jobtemplate',
            name='creator',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='jobtemplate',
            name='domain',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='job_templates', to='ufdl-core.DataDomain'),
        ),
        migrations.AddField(
            model_name='jobtemplate',
            name='framework',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='job_templates', to='ufdl-core.Framework'),
        ),
        migrations.AddField(
            model_name='jobtemplate',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='job_templates', to='ufdl-core.JobType'),
        ),
        migrations.AddField(
            model_name='joboutput',
            name='creator',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='joboutput',
            name='data',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='ufdl-core.File'),
        ),
        migrations.AddField(
            model_name='joboutput',
            name='job',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='outputs', to='ufdl-core.Job'),
        ),
        migrations.AddField(
            model_name='job',
            name='creator',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='docker_image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='jobs', to='ufdl-core.DockerImage'),
        ),
        migrations.AddField(
            model_name='job',
            name='node',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='jobs', to='ufdl-core.Node'),
        ),
        migrations.AddField(
            model_name='job',
            name='template',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='jobs', to='ufdl-core.JobTemplate'),
        ),
        migrations.AddField(
            model_name='input',
            name='template',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='inputs', to='ufdl-core.JobTemplate'),
        ),
        migrations.AddConstraint(
            model_name='hardware',
            constraint=models.UniqueConstraint(fields=('generation',), name='unique_generation_names'),
        ),
        migrations.AddConstraint(
            model_name='framework',
            constraint=models.UniqueConstraint(fields=('name', 'version'), name='unique_frameworks'),
        ),
        migrations.AddField(
            model_name='filereference',
            name='file',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='file_references', to='ufdl-core.NamedFile'),
        ),
        migrations.AddConstraint(
            model_name='filename',
            constraint=models.UniqueConstraint(fields=('filename',), name='unique_filenames'),
        ),
        migrations.AddConstraint(
            model_name='file',
            constraint=models.UniqueConstraint(fields=('handle',), name='unique_file_handles'),
        ),
        migrations.AddConstraint(
            model_name='domain',
            constraint=models.UniqueConstraint(fields=('name',), name='unique_domain_names'),
        ),
        migrations.AddField(
            model_name='dockerimagetojobtype',
            name='docker_image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='ufdl-core.DockerImage'),
        ),
        migrations.AddField(
            model_name='dockerimagetojobtype',
            name='job_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='ufdl-core.JobType'),
        ),
        migrations.AddField(
            model_name='dockerimage',
            name='cuda_version',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='docker_images', to='ufdl-core.CUDAVersion'),
        ),
        migrations.AddField(
            model_name='dockerimage',
            name='framework',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='docker_images', to='ufdl-core.Framework'),
        ),
        migrations.AddField(
            model_name='dockerimage',
            name='domain',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='docker_images', to='ufdl-core.DataDomain'),
        ),
        migrations.AddField(
            model_name='dockerimage',
            name='min_hardware_generation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='ufdl-core.Hardware'),
        ),
        migrations.AddField(
            model_name='dockerimage',
            name='tasks',
            field=models.ManyToManyField(related_name='docker_images', through='ufdl-core.DockerImageToJobType', to='ufdl-core.JobType'),
        ),
        migrations.AddField(
            model_name='dataset',
            name='creator',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='dataset',
            name='files',
            field=models.ManyToManyField(related_name='_dataset_files_+', to='ufdl-core.FileReference'),
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
            model_name='parameter',
            constraint=models.UniqueConstraint(fields=('template', 'name'), name='unique_template_parameter_names'),
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
            model_name='jobtemplate',
            constraint=models.UniqueConstraint(condition=models.Q(deletion_time__isnull=True), fields=('name', 'version'), name='unique_active_job_templates'),
        ),
        migrations.AddConstraint(
            model_name='joboutput',
            constraint=models.UniqueConstraint(fields=('job', 'name'), name='unique_job_output_names'),
        ),
        migrations.AddConstraint(
            model_name='input',
            constraint=models.UniqueConstraint(fields=('template', 'name'), name='unique_template_input_names'),
        ),
        migrations.AddConstraint(
            model_name='dockerimagetojobtype',
            constraint=models.UniqueConstraint(fields=('docker_image', 'job_type'), name='unique_job_types_per_docker_image'),
        ),
        migrations.AddConstraint(
            model_name='dockerimage',
            constraint=models.UniqueConstraint(fields=('name', 'version'), name='unique_docker_images'),
        ),
        migrations.AddConstraint(
            model_name='dataset',
            constraint=models.UniqueConstraint(condition=models.Q(deletion_time__isnull=True), fields=('name', 'version', 'project'), name='unique_active_datasets_per_project'),
        ),
    ]
