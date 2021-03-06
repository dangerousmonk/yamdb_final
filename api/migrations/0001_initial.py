# Generated by Django 3.1.7 on 2021-08-22 08:37

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models

import api.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25, verbose_name='category')),
                ('slug', models.CharField(max_length=50, unique=True, verbose_name='slug')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ['slug'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='comment text')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='publication date')),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
                'ordering': ['-pub_date'],
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25, verbose_name='name')),
                ('slug', models.CharField(max_length=50, unique=True, verbose_name='address')),
            ],
            options={
                'verbose_name': 'Genre',
                'verbose_name_plural': 'Genres',
                'ordering': ['slug'],
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=5, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)], verbose_name='rating')),
                ('text', models.TextField(verbose_name='text')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='pub_date')),
            ],
            options={
                'verbose_name': 'Review',
                'verbose_name_plural': 'Reviews',
                'ordering': ['-pub_date'],
            },
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, verbose_name='name')),
                ('year', models.IntegerField(blank=True, validators=[api.validators.year_validator], verbose_name='year')),
                ('description', models.TextField(verbose_name='description')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='titles', to='api.category', verbose_name='category')),
                ('genre', models.ManyToManyField(blank=True, related_name='titles', to='api.Genre', verbose_name='genre')),
            ],
            options={
                'verbose_name': 'Title',
                'verbose_name_plural': 'Titles',
                'ordering': ['-id'],
            },
        ),
    ]
