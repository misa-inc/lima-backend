import uuid

from extensions.utils import get_random_code
from extensions.utils import MONTH as month

from directory.models import Directory
from page.models import Page
from project.models import Project
from events.models import *

from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext as _
from django.core.validators import RegexValidator
from django.template.defaultfilters import slugify
from django.contrib.admin import display
from django.utils import timezone
from django.db import models

from datetime import date
from rest_framework_simplejwt.tokens import RefreshToken
from taggit.managers import TaggableManager

from .managers import CustomUserManager


def upload_to(instance, filename):
    return "avatars/{0}/{1}".format(instance.username, filename)


def upload_for(instance, filename):
    return "covers/{0}/{1}".format(instance.username, filename)

def badge_to(instance, filename):
    return "badges/{0}/{1}".format(instance.user.username, filename)



def add_user_util(instance):
    now = date.today()
    if not instance.month:
        instance.day = now.day
        instance.month = month[now.month]
        instance.year = now.year
        instance.created = date(day=now.day, month=now.month, year=now.year)


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
        primary_key=True, unique=True, default=uuid.uuid4, editable=False
    )
    avatar = models.ImageField(upload_to=upload_to, blank=True, null=True)
    cover = models.ImageField(upload_to=upload_for, blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=255, unique=True)
    phone_regex = RegexValidator(
        regex=r"/^(\+\d{1,3}\s?)?(\d{1,4}[-.\s]?)(\(\d{1,}\)|\d{1,}[-.\s]?)?(\d{1,}[-.\s]?){1,}\d{1,}$/;", message=_("Invalid phone number."),
    )
    phone = models.CharField(
        max_length=12, validators=[phone_regex], 
        unique=True, verbose_name=_("phone"),
    )
    full_name = models.CharField(
        max_length=100, blank=True, 
        verbose_name=_("full name"),
    )
    bio = models.TextField(blank=True, null=True)
    sex = models.CharField(max_length=32, null=True, blank=True)
    headline = models.CharField(max_length=500, null=True, blank=True)
    call_code = models.CharField(max_length=500, null=True, blank=True)
    otp = models.IntegerField(blank=True, null=True, default=0)
    website = models.CharField(max_length=500, null=True, blank=True)
    country = models.CharField(max_length=500, null=True, blank=True)
    state = models.CharField(max_length=1000, null=True, blank=True)
    address = models.CharField(max_length=1000, null=True, blank=True)
    city = models.CharField(max_length=1000, null=True, blank=True)
    location = models.CharField(max_length=1000, null=True, blank=True)
    total_streak = models.IntegerField(null=True, blank=True)
    total_aura = models.IntegerField(null=True, blank=True)
    day = models.CharField(max_length=3, null=True, blank=True)
    month = models.CharField(max_length=15, null=True, blank=True)
    year = models.CharField(max_length=7, null=True, blank=True)
    postal_code = models.CharField(max_length=50, null=True, blank=True)
    dob = models.CharField(max_length=1000, null=True, blank=True)
    friends = models.ManyToManyField("self", related_name="user_friends", blank=True, symmetrical=False)
    blocked = models.ManyToManyField("self", related_name="user_blocked", blank=True, symmetrical=False)
    open_to_work = models.BooleanField(default=False)
    open_to_collaborate = models.BooleanField(default=False)
    author = models.BooleanField(
        default=False, blank=True, 
        verbose_name=_("author"),
    )
    special_user = models.DateTimeField(
        default=timezone.now, verbose_name=_("Special User"),
    )
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False,)
    is_banned = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False,)
    active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(
        default=timezone.now, verbose_name=_("date joined"),
    )
    two_step_password = models.BooleanField(
        default=False, help_text=_("is active two step password?"),
        verbose_name=_("two step password"),
    )
    slug = models.SlugField(unique=True, blank=True, null=False, max_length=1000)
    tos = models.BooleanField(default=False)
    created = models.CharField(max_length=1000, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    tags = TaggableManager()

    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    @property
    def get_short_name(self):
        return self.username    

    @property
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}

    @property
    def friends_count(self):
        return self.friends.all().count()

    @property
    def blocked_count(self):
        return self.blocked.all().count()

    @property
    def is_directory_member(self):
        return Directory.objects.filter(subscribers=self)

    @property
    def is_diectory_moderator(self):
        return Directory.objects.filter(moderators=self)
    
    @property
    def is_page_member(self):
        return Page.objects.filter(subscribers=self)

    @property
    def is_page_moderator(self):
        return Page.objects.filter(moderators=self)

    @property
    def is_project_member(self):
        return Project.objects.filter(subscribers=self)

    @property
    def is_project_moderator(self):
        return Project.objects.filter(moderators=self)

    @property
    def is_event_member(self):
        return Event.objects.filter(guests=self)

    @display(
        boolean=True,
        description=_("Special User"),
    )
    def is_special_user(self):
        if self.special_user > timezone.now():
            return True
        else:
            return False

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        ex = False
        if self.username:
            to_slug = slugify(str(self.username))
            ex = User.objects.filter(slug=to_slug).exists()
            while ex:
                to_slug = slugify(to_slug + "" + str(get_random_code()))
                ex = User.objects.filter(slug=to_slug).exists()
        else:
            to_slug = str(self.username)
        self.slug = to_slug
        add_user_util(self)
        super().save(*args, **kwargs)            


class Experience(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="experiences", verbose_name=_("User"),
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
        return self.user.username

    class Meta:
        ordering = [
            "-create", "-id",
        ]
        verbose_name = _("Experience")
        verbose_name_plural = _("Experiences")


class Education(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="educations", verbose_name=_("User"),
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
        return self.user.username

    class Meta:
        ordering = [
            "-create", "-id",
        ]
        verbose_name = _("Education")
        verbose_name_plural = _("Educations")

#Record model is a multiple of status by time by score (if its game etc) Minor = 2 and Major = 4
class Record(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="records", verbose_name=_("User"),
    )
    aura = models.CharField(max_length=30000, blank=True, null=True)
    posts = models.ForeignKey(
        'post.Post', on_delete=models.CASCADE, related_name="record_posts", blank=True, default=None
    )#Answering in QnA's, Quizzes, Polls (Minor) --- DONE
    events = models.ForeignKey(
        'events.Event', on_delete=models.CASCADE, related_name="record_events", blank=True, default=None
    )#TODO Participating and attending a competitions (Major), sessions, webinar, meetup, tune (Minor) --- This will be done at the frontend
    publication = models.ForeignKey(
        'blog.Blog', on_delete=models.CASCADE, related_name="record_publication", blank=True, default=None
    )#TODO Reading a Blog (Minor) --- This will be done at the frontend
    books = models.ForeignKey(
        'library.Book', on_delete=models.CASCADE, related_name="record_books", blank=True, default=None
    )#TODO Reading or listening to a book (Minor) --- This will be done at the frontend
    directories = models.ForeignKey(
        'directory.Directory', on_delete=models.CASCADE, related_name="record_directories", blank=True, default=None
    )#TODO Participating in a directory by making requests, deliveries, going through and completing a Branch Environment (Major)
    projects = models.ForeignKey(
        'project.Project', on_delete=models.CASCADE, related_name="record_project", blank=True, default=None
    )#TODO Participating in a directory by making requests, deliveries (Major)
    discussions = models.ForeignKey(
        'discussion.Discussion', on_delete=models.CASCADE, related_name="record_discussions", blank=True, default=None
    )#Participing in a directory discussion by asking or answering in it (Minor) --- DONE
    #TODO Pariticpating in Tryout (Major) --- This will be done at the frontend
    #TODO Pariticpating in Challenges (Major) --- This will be done at the frontend
    #TODO Participating in Games (Major) --- This will be done at the frontend
    time = models.CharField(max_length=100000, blank=True, null=True)#Time in seconds that a user did some record
    type = models.CharField(max_length=300, blank=True, null=True)#Is it a Major or a Minor record
    status = models.CharField(max_length=300, blank=True, null=True)#Is it a ongoing or closed
    description = models.TextField(verbose_name=_("Description"),)
    is_deleted = models.BooleanField(default=False)
    create = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Create time"),
    )
    updated = models.DateTimeField(
        auto_now=True, verbose_name=_("Update time"),
    )

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = [
            "-create", "-id",
        ]
        verbose_name = _("Record")
        verbose_name_plural = _("Records")


class Badge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, default=None)
    image = models.ImageField(
        upload_to=badge_to, blank=True, null=True, max_length=100000
    )
    title = models.CharField(max_length=300)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = [
            "-last_modified", "-id",
        ]
        verbose_name = _("Badge")
        verbose_name_plural = _("Badges")