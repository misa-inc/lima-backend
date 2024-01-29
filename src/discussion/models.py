from django.db import models
from datetime import date, datetime
from django.utils import timezone
from account.models import User 
import random, string , os 
from extensions.utils import get_random_code
from extensions.utils import MONTH as month
from django.conf import settings
from taggit.managers import TaggableManager
from directory.models import Directory
from project.models import Project

#There are two types of discussion a normal lima discussion or a lima request

def bot_to(instance, filename):
    return "bots/{0}/{1}".format(instance.file_name, filename)

def category_to(instance, filename):
    return "categories/{0}/{1}".format(instance.title, filename)


def discussion_to(instance, filename):
    return "discussions/{0}/{1}".format(instance.discussion_name, filename)


def discussion_for(instance, filename):
    return "discussions/{0}/{1}".format(instance.discussion_name, filename)


def file_to(instance, filename):
    return "discussions/{0}/{1}/{2}".format(instance.discussion.discussion_name, instance.from_user.username, filename)


def pluralize(value, unit):
    if value == 1:
        return f'1{unit}'
    return f'{value}{unit}'


def time_ago(dt):
    t = timezone.now() - dt
    if t.days == 0:
        if t.seconds < 60:
            return 'just now'
        if t.seconds < 3600:
            return pluralize(t.seconds//60, 'm')
        if t.seconds < 3600 * 24:
            return pluralize(t.seconds//3600, 'h')
    if t.days < 30:
        return pluralize(t.days, 'd')
    if t.days < 365:
        return pluralize(t.days//30, 'mo')
    return pluralize(t.days//365, 'yr')


def add_discussion_util(instance):
    now = date.today()
    if not instance.month:
        instance.subscriber_count =+ 1
        instance.day = now.day
        instance.month = month[now.month]
        instance.year = now.year
        instance.save()


class Bot(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=33)#Bot name actually
    file = models.FileField(
        upload_to=bot_to, blank=True, null=True, max_length=1000000
    )
    message_handler = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.description or self.file_name
    
    def save(self, *args, **kwargs):
        dirname = os.path.dirname(self.file_name)
        if dirname:
            self.file_name = self.file_name.replace(dirname,'').replace('/','')
        return super().save(*args, **kwargs)


class Category(models.Model):
    avatar = models.ImageField(
        upload_to=category_to, blank=True, null=True, max_length=1000000
    )
    directory = models.ForeignKey(Directory, on_delete=models.CASCADE, related_name='discussiom_category_set', null=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True,null=True)
    needs_answer = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    def __repr__(self):
        return '<title:{}'.format(self.title)    


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
    directory = models.ForeignKey(Directory, on_delete=models.CASCADE, null=True)
    projects = models.ManyToManyField(Project, related_name='project_discussion_set')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    blocked_users = models.ManyToManyField(User, related_name='blocked_users_set')
    liked_users = models.ManyToManyField(User, related_name='liked_users_set')
    subscribed_users = models.ManyToManyField(User, related_name='subscribed_users_set')#TODO Make it so that users who subscribe can recieve notifications in the future
    moderator_users = models.ManyToManyField(User, related_name='moderator_users_set')
    subscriber_count = models.IntegerField(blank=True, null=True, default=0)
    like_count = models.IntegerField(blank=True, null=True, default=0)
    category = models.ForeignKey(Category, related_name='discussion_category', on_delete=models.CASCADE, null=True)
    discussion_type = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)#Its either Open or Closed
    share_count = models.IntegerField(blank=True, null=True, default=0)
    is_request = models.BooleanField(default=False)
    answered = models.BooleanField(default=False)
    active_bots = models.ManyToManyField(Bot) 
    #TODO Add Delivery manytomanyfield
    #TODO Add Branch manytomanyfield
    #TODO Add Milestone manytomanyfield

    labels = TaggableManager()

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
    liked_users = models.ManyToManyField(User, related_name='liked_chats_set')
    day = models.CharField(max_length=3, null=True, blank=True)
    month = models.CharField(max_length=15, null=True, blank=True)
    year = models.CharField(max_length=7, null=True, blank=True)
    time = models.CharField(max_length=15, null=True, blank=True)
    first_chat = models.BooleanField(default=False)

    @property
    def created_time_ago(self):
        return time_ago(self.created)    

    def __repr__(self):
        return '<from_user:{}'.format(self.from_user.username)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
