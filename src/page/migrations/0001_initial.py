# Generated by Django 3.2.8 on 2024-01-15 11:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import page.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(blank=True, max_length=1000000, null=True, upload_to=page.models.page_to)),
                ('cover', models.ImageField(blank=True, max_length=1000000, null=True, upload_to=page.models.page_for)),
                ('name', models.CharField(max_length=250, unique=True)),
                ('description', models.TextField(blank=True, max_length=100000, null=True)),
                ('category', models.CharField(blank=True, max_length=1000, null=True)),
                ('page_type', models.CharField(blank=True, max_length=100, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('day', models.CharField(blank=True, max_length=1000, null=True)),
                ('month', models.CharField(blank=True, max_length=1000, null=True)),
                ('year', models.CharField(blank=True, max_length=1000, null=True)),
                ('subscriber_count', models.IntegerField(blank=True, default=0, null=True)),
                ('share_count', models.IntegerField(blank=True, default=0, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('slug', models.SlugField(blank=True, max_length=1000, unique=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='page_creator', to=settings.AUTH_USER_MODEL)),
                ('moderators', models.ManyToManyField(blank=True, default=None, related_name='moderators', to=settings.AUTH_USER_MODEL)),
                ('subscribers', models.ManyToManyField(blank=True, default=None, related_name='subscribers', to=settings.AUTH_USER_MODEL)),
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
                ('page', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='page.page')),
            ],
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, max_length=100000, null=True, upload_to=page.models.link_to)),
                ('title', models.CharField(max_length=300)),
                ('url', models.URLField(blank=True, max_length=2000)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('page', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='page.page')),
            ],
        ),
    ]
