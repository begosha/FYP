# Generated by Django 4.1.7 on 2023-03-08 07:46

import calculator.mixins
import calculator.models
from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('file', models.FileField(blank=True, max_length=255, null=True, upload_to='', verbose_name='File')),
                ('description', models.TextField(blank=True, default='', verbose_name='Description')),
                ('meta', models.JSONField(blank=True, null=True, verbose_name='Meta')),
            ],
            options={
                'db_table': 'file',
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Position name')),
                ('price', models.IntegerField(blank=True, null=True, verbose_name='Position Price')),
            ],
            options={
                'verbose_name': 'Position',
                'verbose_name_plural': 'Positions',
                'db_table': 'position',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('total_check', models.JSONField(blank=True, null=True, verbose_name='Total Check')),
                ('position', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transactions', related_query_name='transaction', to='calculator.position', verbose_name='Transaction')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transactions', related_query_name='transaction', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'get_latest_by': '-pk',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Scan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                ('image', calculator.models.FileField(blank=True, help_text='Image taken or uploaded', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='scan', to='calculator.file', verbose_name='Scan')),
                ('position', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='scans', related_query_name='scan', to='calculator.position', verbose_name='Position')),
            ],
            options={
                'verbose_name': 'Scan',
                'verbose_name_plural': 'Scans',
                'db_table': 'scan',
            },
            bases=(calculator.mixins.FileUploadToMixin, models.Model),
        ),
        migrations.CreateModel(
            name='PositionFeatureVector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                ('feature_vector', django.contrib.postgres.fields.ArrayField(base_field=models.PositiveBigIntegerField(), blank=True, default=list, size=None, verbose_name='Position feature vectors')),
                ('file', calculator.models.FileField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='featurevector', to='calculator.file', verbose_name='File')),
                ('position', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='featurevectors', related_query_name='featurevector', to='calculator.position', verbose_name='Position')),
            ],
            options={
                'verbose_name': 'Position feature vector',
                'verbose_name_plural': 'Position feature vectors',
                'db_table': 'positionfeaturevector',
            },
        ),
        migrations.CreateModel(
            name='BoundingBox',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                ('coordinates', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=2), blank=True, null=True, size=None, verbose_name='Coordinates')),
                ('position', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bboxes', related_query_name='bbox', to='calculator.position', verbose_name='Position')),
                ('scan', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bboxes', related_query_name='bbox', to='calculator.scan', verbose_name='Scan')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
