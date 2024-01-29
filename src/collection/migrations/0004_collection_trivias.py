# Generated by Django 3.2.8 on 2024-01-29 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('collection', '0003_initial'),
        ('trivia', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='trivias',
            field=models.ManyToManyField(blank=True, default=None, related_name='trivias', to='trivia.Trivia'),
        ),
    ]
