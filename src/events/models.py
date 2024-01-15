import datetime

from django.db import models
from django.utils import timezone
from django.utils.safestring import mark_safe

from account.models import User

#TODO Add more event fields as time goes on


def link_to(instance, filename):
    return "start_competition/{0}/{1}".format(instance.title, filename)

def event_for(instance, filename):
    return "events/{0}/{1}".format(instance.title, filename)


class Event(models.Model):
    title=models.CharField(max_length=300)
    description=models.TextField(default="description")
    date_created=models.DateTimeField(auto_now_add=True)
    preview=models.ImageField(upload_to=event_for, blank=True, null=True, max_length=1000000)
    location_type=models.CharField(max_length=100,default="PHYSICAL")#PHYSICAL OR ONLINE
    type=models.CharField(max_length=100,default="PRIVATE")#PRIVATE OR PUBLIC
    virtual_type=models.CharField(max_length=100,default="AUDIO")#AUDIO OR VIDEO CONFERENCE OR COMPETITION OR WEBINAR ETC
    code_adhesion=models.CharField(max_length=20,default="")
    challenge = models.TextField(blank=True)
    judging_criteria = models.TextField(blank=True)
    category=models.CharField(max_length=20000,default="")
    owner=models.ForeignKey(User,on_delete=models.CASCADE)
    start_date = models.DateTimeField(verbose_name="start_date",default=datetime.datetime.now())
    end_date=models.DateTimeField(verbose_name="end_date", default=(timezone.now() + datetime.timedelta(hours=1)))
    end_date_inscription = models.DateTimeField(verbose_name="end_date_inscription")
    status=models.CharField(max_length=100,default="ACTIVE")#ACTIVE, CLOSED, 
    guests = models.ManyToManyField(User, through='Guest',related_name="guests")
    city = models.CharField(max_length=255,default="lima")
    county = models.CharField(max_length=255,default="lima")
    state = models.CharField(max_length=255,default="lima")
    country = models.CharField(max_length=255,default="lima")
    location = models.CharField(max_length=255,default="lima")#The location for the PHYSICAL event
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Prize(models.Model):#Prizes for the competition
    event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=True, default=None)
    image = models.ImageField(
        upload_to=link_to, blank=True, null=True, max_length=100000
    )
    title = models.CharField(max_length=3000)
    url = models.URLField(blank=True, max_length=2000)
    last_modified = models.DateTimeField(auto_now=True)


class Acknowledgement(models.Model):#Where the data was gotten from for the competition
    event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=True, default=None)
    image = models.ImageField(
        upload_to=link_to, blank=True, null=True, max_length=100000
    )
    title = models.CharField(max_length=3000)
    url = models.URLField(blank=True, max_length=2000)
    last_modified = models.DateTimeField(auto_now=True)


class Step(models.Model):#How to start the competition
    event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=True, default=None)
    image = models.ImageField(
        upload_to=link_to, blank=True, null=True, max_length=100000
    )
    title = models.CharField(max_length=3000)
    url = models.URLField(blank=True, max_length=2000)
    last_modified = models.DateTimeField(auto_now=True)


class Rule(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=True, default=None)
    title = models.CharField(max_length=3000)
    text = models.TextField(blank=True)
    last_modified = models.DateTimeField(auto_now=True)


class Guest(models.Model):#Entrees
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=255,default="STATUS")
    feedback = models.TextField(default="feedback")
    rating = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return  f"Invited {self.user} for {self.event}"

