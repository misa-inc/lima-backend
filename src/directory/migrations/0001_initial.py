# Generated by Django 3.2.8 on 2024-01-29 04:58

import directory.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Directory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(blank=True, max_length=1000000, null=True, upload_to=directory.models.directory_to)),
                ('cover', models.ImageField(blank=True, max_length=1000000, null=True, upload_to=directory.models.directory_for)),
                ('name', models.CharField(max_length=250, unique=True)),
                ('about', models.TextField(blank=True, max_length=100000, null=True)),
                ('description', models.TextField(blank=True, max_length=100000, null=True)),
                ('code_of_conduct', models.TextField(blank=True, max_length=100000, null=True)),
                ('category', models.CharField(blank=True, max_length=1000, null=True)),
                ('directory_type', models.CharField(blank=True, max_length=100, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('day', models.CharField(blank=True, max_length=1000, null=True)),
                ('month', models.CharField(blank=True, max_length=1000, null=True)),
                ('year', models.CharField(blank=True, max_length=1000, null=True)),
                ('subscriber_count', models.IntegerField(blank=True, default=0, null=True)),
                ('share_count', models.IntegerField(blank=True, default=0, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('slug', models.SlugField(blank=True, max_length=1000, unique=True)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='Text',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('text', models.TextField(blank=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('directory', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='directory.directory')),
            ],
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, max_length=100000, null=True, upload_to=directory.models.link_to)),
                ('title', models.CharField(max_length=300)),
                ('url', models.URLField(blank=True, max_length=2000)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('directory', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='directory.directory')),
            ],
        ),
    ]
