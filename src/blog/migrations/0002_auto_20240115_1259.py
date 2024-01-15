# Generated by Django 3.2.8 on 2024-01-15 11:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=20, null=True, verbose_name='Name')),
                ('object_id', models.PositiveIntegerField(verbose_name='object id')),
                ('category', models.CharField(blank=True, max_length=300, null=True)),
                ('perspective', models.CharField(blank=True, max_length=300, null=True)),
                ('body', models.TextField(verbose_name='Body')),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_reviewed', models.BooleanField(default=False)),
                ('has_perspective', models.BooleanField(default=False)),
                ('create', models.DateTimeField(auto_now_add=True, verbose_name='Create time')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Update time')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='contenttypes.contenttype', verbose_name='content type')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='blog.comment', verbose_name='parent')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
                'ordering': ['-create', '-id'],
            },
        ),
        migrations.AddField(
            model_name='blog',
            name='has_perspective',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='blog',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='blog',
            name='is_reviewed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='blog',
            name='perspective',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.RemoveField(
            model_name='blog',
            name='category',
        ),
        migrations.AddField(
            model_name='blog',
            name='category',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
