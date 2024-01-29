# Generated by Django 3.2.8 on 2024-01-29 04:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import feedback.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('text', models.TextField(blank=True, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('share_count', models.IntegerField(blank=True, default=0, null=True)),
                ('votes', models.IntegerField(default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedback_comment_author', to=settings.AUTH_USER_MODEL)),
                ('parent_comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='feedback.comment')),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('attachment', models.ImageField(blank=True, max_length=100000, null=True, upload_to=feedback.models.post_to)),
                ('video', models.FileField(blank=True, max_length=1000000, null=True, upload_to=feedback.models.post_to)),
                ('file', models.FileField(blank=True, max_length=1000000, null=True, upload_to=feedback.models.post_to)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('link', models.URLField(blank=True, max_length=2000, null=True)),
                ('text', models.TextField(blank=True, max_length=100000, null=True)),
                ('board', models.CharField(blank=True, max_length=300, null=True)),
                ('status', models.CharField(blank=True, max_length=300, null=True)),
                ('post_type', models.CharField(blank=True, max_length=300, null=True)),
                ('share_count', models.IntegerField(blank=True, default=0, null=True)),
                ('saved_count', models.IntegerField(blank=True, default=0, null=True)),
                ('report_count', models.IntegerField(blank=True, default=0, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_repost', models.BooleanField(default=False)),
                ('is_reviewed', models.BooleanField(default=True)),
                ('votes', models.IntegerField(default=0)),
                ('reposts', models.IntegerField(default=0)),
                ('comments', models.IntegerField(default=0)),
                ('slug', models.SlugField(blank=True, max_length=1000)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedback_author', to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='alt', to='feedback.feedback')),
                ('report', models.ManyToManyField(blank=True, default=None, related_name='feedback_report', to=settings.AUTH_USER_MODEL)),
                ('saved', models.ManyToManyField(blank=True, default=None, related_name='feedback_saved', to=settings.AUTH_USER_MODEL)),
                ('voters', models.ManyToManyField(related_name='feedback_voters', to=settings.AUTH_USER_MODEL)),
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
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField()),
                ('is_post', models.BooleanField()),
                ('is_comment', models.BooleanField()),
                ('comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='feedback.comment')),
                ('post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='feedback.feedback')),
                ('voter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='voter', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='feedback.feedback'),
        ),
        migrations.AddField(
            model_name='comment',
            name='report',
            field=models.ManyToManyField(blank=True, default=None, related_name='feedback_comment_report', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='saved',
            field=models.ManyToManyField(blank=True, default=None, related_name='feedback_comment_saved', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='voters',
            field=models.ManyToManyField(related_name='feedback_comment_voters', to=settings.AUTH_USER_MODEL),
        ),
    ]
