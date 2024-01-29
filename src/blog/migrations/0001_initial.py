# Generated by Django 3.2.8 on 2024-01-29 04:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import extensions.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
                ('likes', models.ManyToManyField(blank=True, related_name='comments_like', to=settings.AUTH_USER_MODEL, verbose_name='Likes')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='blog.comment', verbose_name='parent')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
                'ordering': ['-create', '-id'],
            },
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(blank=True, max_length=300, null=True)),
                ('perspective', models.CharField(blank=True, max_length=300, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_reviewed', models.BooleanField(default=False)),
                ('has_perspective', models.BooleanField(default=False)),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('slug', models.SlugField(blank=True, help_text='Do not fill in here', unique=True, verbose_name='Slug')),
                ('body', models.TextField(verbose_name='Content')),
                ('image', models.ImageField(blank=True, null=True, upload_to=extensions.utils.upload_file_path, verbose_name='Image')),
                ('summary', models.TextField(max_length=400, verbose_name='Summary')),
                ('publish', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Publish time')),
                ('create', models.DateTimeField(auto_now_add=True, verbose_name='Create time')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Update time')),
                ('special', models.BooleanField(default=False, verbose_name='Is special Blog ?')),
                ('status', models.CharField(max_length=1, verbose_name='Status')),
                ('visits', models.PositiveIntegerField(default=0, verbose_name='Visits')),
                ('author', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='blogs', to=settings.AUTH_USER_MODEL, verbose_name='Author')),
            ],
            options={
                'verbose_name': 'Blog',
                'verbose_name_plural': 'Blogs',
                'ordering': ['-publish', '-updated'],
            },
        ),
    ]
