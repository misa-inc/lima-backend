from django.db import models
from datetime import date, datetime
from django.utils import timezone
from account.models import User 
import random, string , os 
from extensions.utils import get_random_code
from extensions.utils import MONTH as month
from django.conf import settings



def discussion_to(instance, filename):
    return "discussions/{0}/{1}".format(instance.discussion_name, filename)


def discussion_for(instance, filename):
    return "discussions/{0}/{1}".format(instance.discussion_name, filename)


def file_to(instance, filename):
    return "discussions/{0}/{1}/{2}".format(instance.discussion.discussion_name, instance.from_user.username, filename)


def add_discussion_util(instance):
    now = date.today()
    if not instance.month:
        instance.subscriber_count =+ 1
        instance.day = now.day
        instance.month = month[now.month]
        instance.year = now.year
        instance.save()


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


class Bot(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=33)
    message_handler = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.description or self.file_name
    
    def save(self, *args, **kwargs):
        dirname = os.path.dirname(self.file_name)
        if dirname:
            self.file_name = self.file_name.replace(dirname,'').replace('/','')
        return super().save(*args, **kwargs)


class Discussion(models.Model):
    avatar = models.ImageField(
        upload_to=discussion_to, blank=True, null=True, max_length=1000000
    )
    cover = models.ImageField(
        upload_to=discussion_for, blank=True, null=True, max_length=1000000
    )
    discussion_code = models.CharField(max_length=8)
    discussion_name = models.CharField(max_length=255)
    day = models.CharField(max_length=1000, null=True, blank=True)
    month = models.CharField(max_length=1000, null=True, blank=True)
    year = models.CharField(max_length=1000, null=True, blank=True)
    about = models.TextField(blank=True, null=True, max_length=100000)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    blocked_users = models.ManyToManyField(User, related_name='blocked_users_set')
    subscribed_users = models.ManyToManyField(User, related_name='subscribed_users_set')
    moderator_users = models.ManyToManyField(User, related_name='moderator_users_set')
    subscriber_count = models.IntegerField(blank=True, null=True, default=0)
    category = models.CharField(max_length=1000, null=True, blank=True)
    discussion_type = models.CharField(max_length=100, null=True, blank=True)
    share_count = models.IntegerField(blank=True, null=True, default=0)
    active_bots = models.ManyToManyField(Bot) 

    def save(self, discussion_code=True, *args, **kwargs):
        if not discussion_code:
            self.discussion_code = self.__generate_code()
        add_discussion_util(self)
        super().save(*args, **kwargs)
    
    @property
    def online_count(self):
        return self.subscribers.filter(active=True).count()

    def __repr__(self):
        return self.discussion_name
    
    def __str__(self):
        return self.discussion_name

    def __generate_code(self):
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(8))


class Visitor(models.Model):
    user_agent = models.TextField(null=True)
    ip_addr = models.GenericIPAddressField()

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    def __repr__(self):
        return '<user_agent:{}'.format(self.user_agent)    


class Chat(models.Model):
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, null=True)
    file = models.FileField(
        upload_to=file_to, blank=True, null=True, max_length=1000000
    )
    from_user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(null=False)
    created = models.DateTimeField(default=timezone.now)
    day = models.CharField(max_length=3, null=True, blank=True)
    month = models.CharField(max_length=15, null=True, blank=True)
    year = models.CharField(max_length=7, null=True, blank=True)
    time = models.CharField(max_length=15, null=True, blank=True)
    
    def __repr__(self):
        return '<from_user:{}'.format(self.from_user.username)
    
    def save(self, *args, **kwargs):
        time_n_day_ago(self)
        super().save(*args, **kwargs)
