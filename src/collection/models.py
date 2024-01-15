import uuid

from django.db import models, transaction
from django.core.files import File
from django.db.models import Sum
from django.core.exceptions import FieldError
from django.contrib.auth.models import Permission
from django.utils.text import slugify
from django.utils import timezone
from datetime import date

from guardian.shortcuts import assign_perm
from extensions.utils import get_random_code
from extensions.utils import MONTH as month
# TODO Add more details to page


def link_to(instance, filename):
    return "links/{0}/{1}".format(instance.title, filename)


def post_to(instance, filename):
    return "posts/{0}/{1}".format(instance.title, filename)


def collection_to(instance, filename):
    return "avatars/{0}/{1}".format(instance.name, filename)


def collection_for(instance, filename):
    return "covers/{0}/{1}".format(instance.name, filename)


def get_perm(codename):
    return Permission.objects.get(content_type__app_label="lima", codename=codename)


def get_model_perms():
    perms = []
    for op in ["change", "delete"]:
        for model_name in ["comment", "post"]:
            perms.append(get_perm(f"{op}_{model_name}"))
    return perms


def pluralize(value, unit):
    if value == 1:
        return f"1{unit}"
    return f"{value}{unit}"


def time_ago(dt):
    t = timezone.now() - dt
    if t.days == 0:
        if t.seconds < 60:
            return "just now"
        if t.seconds < 3600:
            return pluralize(t.seconds // 60, "m")
        if t.seconds < 3600 * 24:
            return pluralize(t.seconds // 3600, "h")
    if t.days < 30:
        return pluralize(t.days, "d")
    if t.days < 365:
        return pluralize(t.days // 30, "mo")
    return pluralize(t.days // 365, "yr")


def pluralize(value, unit):
    if value == 1:
        return f"1{unit}"
    return f"{value}{unit}"


def time_ago(dt):
    t = timezone.now() - dt
    if t.days == 0:
        if t.seconds < 60:
            return "just now"
        if t.seconds < 3600:
            return pluralize(t.seconds // 60, "m")
        if t.seconds < 3600 * 24:
            return pluralize(t.seconds // 3600, "h")
    if t.days < 30:
        return pluralize(t.days, "d")
    if t.days < 365:
        return pluralize(t.days // 30, "mo")
    return pluralize(t.days // 365, "yr")


def edited(model):
    td = model.text.last_modified - model.created
    return td.days > -1 and td.seconds > 60 * 5

def add_collection_util(instance):
    now = date.today()
    if not instance.month:
        instance.day = now.day
        instance.month = month[now.month]
        instance.year = now.year
        instance.save()
        


class Text(models.Model):
    text = models.TextField(blank=True)
    last_modified = models.DateTimeField(auto_now=True)


class Collection(models.Model):
    name = models.CharField(max_length=250, unique=True)
    description = models.TextField(blank=True, null=True, max_length=100000)
    collection_type = models.CharField(max_length=100, null=True, blank=True)#Private or Public
    creator = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name="collection_creator")
    posts = models.ManyToManyField(
        'post.Post', related_name="posts", blank=True, default=None
    )
    trivias = models.ManyToManyField(
        'trivia.Trivia', related_name="trivias", blank=True, default=None
    )
    competitions = models.ManyToManyField(
        'events.Event', related_name="competitions", blank=True, default=None
    )
    events = models.ManyToManyField(
        'events.Event', related_name="events", blank=True, default=None
    )
    articles = models.ManyToManyField(
        'blog.Blog', related_name="articles", blank=True, default=None
    )
    books = models.ManyToManyField(
        'library.Book', related_name="books", blank=True, default=None
    )
    directories = models.ManyToManyField(
        'directory.Directory', related_name="directories", blank=True, default=None
    )
    discussions = models.ManyToManyField(
        'discussion.Discussion', related_name="discussions", blank=True, default=None
    )
    created = models.DateTimeField(auto_now_add=True)
    day = models.CharField(max_length=1000, null=True, blank=True)
    month = models.CharField(max_length=1000, null=True, blank=True)
    year = models.CharField(max_length=1000, null=True, blank=True)
    share_count = models.IntegerField(blank=True, null=True, default=0)
    is_deleted = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, blank=True, null=False, max_length=1000)

    
    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return "Collection ---" + self.name

    def save(self, *args, **kwargs):
        ex = False
        if self.name:
            to_slug = slugify(str(self.name))
            ex = Collection.objects.filter(slug=to_slug).exists()
            while ex:
                to_slug = slugify(to_slug + "" + str(get_random_code()))
                ex = Collection.objects.filter(slug=to_slug).exists()
        else:
            to_slug = str(self.name)
        self.slug = to_slug    
        add_collection_util(self)
        super().save(*args, **kwargs)  

