from django.db import models
from django.utils.translation import ugettext as _

from datetime import date, datetime
from django.utils import timezone
from extensions.utils import MONTH as month
from account.models import User
from taggit.managers import TaggableManager


def file_to(instance, filename):
    return "newsletter/{0}/{1}".format(instance.name, filename)


def post_to(instance, filename):
    return "article/{0}/{1}/{2}".format(instance.newsletter.name, instance.name, filename)


def time_n_day_ago(instance):
    now = datetime.now()
    today = date.today()
    current_hour = now.strftime("%H")
    current_minutes = now.strftime("%M")
    instance.day = today.day
    instance.month = month[today.month]
    instance.year = today.year
    if current_hour == "01":
        instance.time = f'1:{current_minutes} AM'
    elif current_hour == "02":
       instance.time = f'2:{current_minutes} AM'
    elif current_hour == "03":
       instance.time = f'3:{current_minutes} AM'
    elif current_hour == "04":
       instance.time = f'4:{current_minutes} AM'
    elif current_hour == "05":
       instance.time = f'5:{current_minutes} AM'
    elif current_hour == "06":
       instance.time = f'6:{current_minutes} AM'
    elif current_hour == "07":
       instance.time = f'7:{current_minutes} AM'
    elif current_hour == "08":
       instance.time = f'8:{current_minutes} AM'
    elif current_hour == "09":
       instance.time = f'9:{current_minutes} AM'
    elif current_hour == "10":
        instance.time = f'10:{current_minutes} AM'
    elif current_hour == "11":
        instance.time = f'11:{current_minutes} AM'
    elif current_hour == "12":
        instance.time = f'12:{current_minutes} PM'
    elif current_hour == "13":
       instance.time = f'1:{current_minutes} PM'
    elif current_hour == "14":
       instance.time = f'2:{current_minutes} PM'
    elif current_hour == "15":
       instance.time = f'3:{current_minutes} PM'
    elif current_hour == "16":
       instance.time = f'4:{current_minutes} PM'
    elif current_hour == "17":
       instance.time = f'5:{current_minutes} PM'
    elif current_hour == "18":
       instance.time = f'6:{current_minutes} PM'
    elif current_hour == "19":
       instance.time = f'7:{current_minutes} PM'
    elif current_hour == "20":
       instance.time = f'8:{current_minutes} PM'
    elif current_hour == "21":
       instance.time = f'9:{current_minutes} PM'
    elif current_hour == "22":
        instance.time = f'10:{current_minutes} PM'
    elif current_hour == "23":
        instance.time = f'11:{current_minutes} PM'
    else:
        instance.time = f'12:{current_minutes} AM'


class Newsletter(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    cover = models.ImageField(
        upload_to=file_to, blank=True, null=True, max_length=1000000
    )
    target = models.ManyToManyField(User, related_name='news_target', blank=True)
    frequency = models.CharField(max_length=50, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='news_likes', blank=True)
    owner = models.ForeignKey(User, related_name='news_owner', on_delete=models.CASCADE, null=True)
    subscribers = models.ManyToManyField(User, related_name='news_subscribers', blank=True)
    category = models.CharField(max_length=3, null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)
    day = models.CharField(max_length=3, null=True, blank=True)
    month = models.CharField(max_length=15, null=True, blank=True)
    year = models.CharField(max_length=7, null=True, blank=True)
    time = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        time_n_day_ago(self)
        super().save(*args, **kwargs)


class Article(models.Model):
    name = models.CharField(max_length=100)
    content = models.TextField()
    cover = models.ImageField(
        upload_to=post_to, blank=True, null=True, max_length=1000000
    )
    newsletter = models.ForeignKey(Newsletter, on_delete=models.CASCADE, related_name='newsletter')
    created = models.DateTimeField(default=timezone.now)
    day = models.CharField(max_length=3, null=True, blank=True)
    month = models.CharField(max_length=15, null=True, blank=True)
    year = models.CharField(max_length=7, null=True, blank=True)
    time = models.CharField(max_length=15, null=True, blank=True)

    tags = TaggableManager()

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        time_n_day_ago(self)
        super().save(*args, **kwargs)        