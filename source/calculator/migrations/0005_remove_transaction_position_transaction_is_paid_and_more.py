# Generated by Django 4.1.7 on 2023-04-17 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0004_position_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='position',
        ),
        migrations.AddField(
            model_name='transaction',
            name='is_paid',
            field=models.BooleanField(default=False, verbose_name='is paid'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='positions',
            field=models.JSONField(null=True),
        ),
    ]
