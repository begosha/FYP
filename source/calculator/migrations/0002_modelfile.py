# Generated by Django 4.1.7 on 2023-05-05 13:20

import calculator.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModelFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Position name')),
                ('model', calculator.models.FileField(blank=True, help_text='Trained model', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='modelfile', to='calculator.file', verbose_name='ModelFile')),
            ],
            options={
                'verbose_name': 'Model File',
                'verbose_name_plural': 'Model Files',
                'db_table': 'modelfile',
            },
        ),
    ]