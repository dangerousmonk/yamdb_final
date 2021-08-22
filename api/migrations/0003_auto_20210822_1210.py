# Generated by Django 3.1.7 on 2021-08-22 09:10

from django.db import migrations, models

import api.validators


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20210822_1137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.IntegerField(blank=True, null=True, validators=[api.validators.year_validator], verbose_name='year'),
        ),
    ]