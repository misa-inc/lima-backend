import uuid

from django.db import models, transaction
from django.core.files import File
from django.db.models import Sum
from django.core.exceptions import FieldError
from django.contrib.auth.models import Permission
from django.utils.text import slugify
from django.utils import timezone
from django.utils.translation import gettext as _
from datetime import date

from guardian.shortcuts import assign_perm
from extensions.utils import get_random_code
from extensions.utils import MONTH as month
from taggit.managers import TaggableManager
# TODO Add more details to page --- page apps & games, advanced settings


def link_to(instance, filename):
    return "links/{0}/{1}".format(instance.title, filename)


def post_to(instance, filename):
    return "posts/{0}/{1}".format(instance.title, filename)


def page_to(instance, filename):
    return "avatars/{0}/{1}".format(instance.name, filename)


def page_for(instance, filename):
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

def add_page_util(instance):
    now = date.today()
    if not instance.month:
        instance.subscriber_count =+ 1
        instance.day = now.day
        instance.month = month[now.month]
        instance.year = now.year
        instance.save()

        
def add_page_utils(instance):    
    creator = instance.creator
    instance.subscribers.add(creator)
    instance.moderators.add(creator)
    instance.save()        


class Text(models.Model):
    text = models.TextField(blank=True)
    last_modified = models.DateTimeField(auto_now=True)


class Page(models.Model):
    avatar = models.ImageField(
        upload_to=page_to, blank=True, null=True, max_length=1000000
    )
    cover = models.ImageField(
        upload_to=page_for, blank=True, null=True, max_length=1000000
    )
    name = models.CharField(max_length=250, unique=True)
    about = models.TextField(blank=True, null=True, max_length=100000)
    description = models.TextField(blank=True, null=True, max_length=100000)
    address = models.TextField(blank=True, null=True, max_length=100000)
    location = models.TextField(blank=True, null=True, max_length=100000)
    category = models.CharField(max_length=1000, null=True, blank=True)
    mobile = models.CharField(max_length=1000, null=True, blank=True)
    email = models.CharField(max_length=1000, null=True, blank=True)
    price = models.CharField(max_length=1000, null=True, blank=True)
    page_type = models.CharField(max_length=100, null=True, blank=True)
    likes = models.ManyToManyField(
        'account.User', related_name="pages_likes", blank=True, default=None
    )
    subscribers = models.ManyToManyField(
        'account.User', related_name="pages_subscribers", blank=True, default=None
    )
    moderators = models.ManyToManyField(
        'account.User', related_name="pages_moderators", blank=True, default=None
    )
    directories = models.ManyToManyField(
        'directory.directory', related_name="pages_directories", blank=True, default=None
    )
    projects = models.ManyToManyField(
        'project.Project', related_name="pages_projects", blank=True, default=None
    )
    books = models.ManyToManyField(
        'library.Book', related_name="pages_books", blank=True, default=None
    )
    creator = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name="page_creator")
    created = models.DateTimeField(auto_now_add=True)
    day = models.CharField(max_length=1000, null=True, blank=True)
    month = models.CharField(max_length=1000, null=True, blank=True)
    year = models.CharField(max_length=1000, null=True, blank=True)
    hours = models.CharField(max_length=1000, null=True, blank=True)
    subscriber_count = models.IntegerField(blank=True, null=True, default=0)
    likes_count = models.IntegerField(blank=True, null=True, default=0)
    share_count = models.IntegerField(blank=True, null=True, default=0)
    is_deleted = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, blank=True, null=False, max_length=1000)

    tags = TaggableManager()

    @property
    def numPosts(self):
        return self.post_set.all().count()
    
    @property
    def online_count(self):
        return self.subscribers.filter(active=True).count()
    
    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return "page ---" + self.name

    def save(self, *args, **kwargs):
        ex = False
        if self.name:
            to_slug = slugify(str(self.name))
            ex = Page.objects.filter(slug=to_slug).exists()
            while ex:
                to_slug = slugify(to_slug + "" + str(get_random_code()))
                ex = Page.objects.filter(slug=to_slug).exists()
        else:
            to_slug = str(self.name)
        self.slug = to_slug    
        add_page_util(self)
        super().save(*args, **kwargs)  


class Link(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, blank=True, default=None)
    image = models.ImageField(
        upload_to=link_to, blank=True, null=True, max_length=100000
    )
    title = models.CharField(max_length=300)
    url = models.URLField(blank=True, max_length=2000)
    last_modified = models.DateTimeField(auto_now=True)


class Rule(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, blank=True, default=None)
    title = models.CharField(max_length=300)
    text = models.TextField(blank=True)
    last_modified = models.DateTimeField(auto_now=True)


class Social(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, blank=True, default=None)
    title = models.CharField(max_length=300)
    url = models.URLField(blank=True, max_length=2000)
    last_modified = models.DateTimeField(auto_now=True)


class Education(models.Model):
    page = models.ForeignKey(
        Page, on_delete=models.CASCADE,
        related_name="pages_educations", verbose_name=_("Page"),
    )
    company = models.CharField(
        max_length=20, null=True, 
        blank=True, verbose_name=_("Company"),
    )
    duration = models.CharField(max_length=300, blank=True, null=True)
    school = models.CharField(max_length=300, blank=True, null=True)
    address = models.CharField(max_length=10000, blank=True, null=True)
    location = models.CharField(max_length=10000, blank=True, null=True)
    start_at = models.CharField(max_length=300, blank=True, null=True)
    end_at = models.CharField(max_length=300, blank=True, null=True)
    school_url = models.URLField(max_length=10000, blank=True, null=True)
    description = models.TextField(verbose_name=_("Description"),)
    is_deleted = models.BooleanField(default=False)
    create = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Create time"),
    )
    updated = models.DateTimeField(
        auto_now=True, verbose_name=_("Update time"),
    )

    def __str__(self):
        return self.page.name

    class Meta:
        ordering = [
            "-create", "-id",
        ]
        verbose_name = _("Education")
        verbose_name_plural = _("Educations")


class Experience(models.Model):
    page = models.ForeignKey(
        Page, on_delete=models.CASCADE,
        related_name="pages_experiences", verbose_name=_("Page"),
    )
    company = models.CharField(
        max_length=20, null=True, 
        blank=True, verbose_name=_("Company"),
    )
    duration = models.CharField(max_length=300, blank=True, null=True)
    title = models.CharField(max_length=300, blank=True, null=True)
    description = models.TextField(verbose_name=_("Description"),)
    is_deleted = models.BooleanField(default=False)
    create = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Create time"),
    )
    updated = models.DateTimeField(
        auto_now=True, verbose_name=_("Update time"),
    )

    def __str__(self):
        return self.page.name

    class Meta:
        ordering = [
            "-create", "-id",
        ]
        verbose_name = _("Experience")
        verbose_name_plural = _("Experiences")