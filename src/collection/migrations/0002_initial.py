# Generated by Django 3.2.8 on 2024-01-29 04:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('directory', '0001_initial'),
        ('discussion', '0001_initial'),
        ('events', '0001_initial'),
        ('library', '0001_initial'),
        ('collection', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='books',
            field=models.ManyToManyField(blank=True, default=None, related_name='books', to='library.Book'),
        ),
        migrations.AddField(
            model_name='collection',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='collection_creator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='collection',
            name='directories',
            field=models.ManyToManyField(blank=True, default=None, related_name='directories', to='directory.Directory'),
        ),
        migrations.AddField(
            model_name='collection',
            name='discussions',
            field=models.ManyToManyField(blank=True, default=None, related_name='discussions', to='discussion.Discussion'),
        ),
        migrations.AddField(
            model_name='collection',
            name='events',
            field=models.ManyToManyField(blank=True, default=None, related_name='events', to='events.Event'),
        ),
    ]
