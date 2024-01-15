from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import models

from extensions.utils import upload_file_path
from account.models import User

from .managers import BlogManager,  CommentManager


# Create your models here.



class Blog(models.Model):
    STATUS_CHOICES = (
        ("p", "publish"),
        ("d", "draft"),
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        default=None, null=False, 
        blank=False, related_name="blogs",
        verbose_name=_("Author"),
    )
    category = models.CharField(max_length=300, blank=True, null=True)
    perspective = models.CharField(max_length=300, blank=True, null=True)
    body = models.TextField(verbose_name=_("Body"),)
    is_deleted = models.BooleanField(default=False)
    is_reviewed = models.BooleanField(default=False)
    has_perspective = models.BooleanField(default=False)
    title = models.CharField(
        max_length=200, verbose_name=_("Title"),
    )
    slug = models.SlugField(
        unique=True, blank=True,
        help_text=_("Do not fill in here"), verbose_name=_("Slug"), 
    )
    body = models.TextField(
        blank=False, verbose_name=_("Content"),
    )
    image = models.ImageField(
        upload_to=upload_file_path, blank=True,
        null=True, verbose_name=_("Image"),
    )
    summary = models.TextField(
        max_length=400, verbose_name=_("Summary"),
    )
    likes = models.ManyToManyField(
        User, blank=True,
        related_name="blogs_like", verbose_name=_("Likes"),
    )
    publish = models.DateTimeField(
        default=timezone.now, verbose_name=_("Publish time"),
    )
    create = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Create time"),
    )
    updated = models.DateTimeField(
        auto_now=True, verbose_name=_("Update time"),
    )
    special = models.BooleanField(
        default=False, verbose_name=_("Is special Blog ?"),
    )
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, 
        verbose_name=_("Status"),
    )
    visits = models.PositiveIntegerField(
        default=0, verbose_name=_("Visits"),
    )

    def __str__(self):
        return f"{self.author.first_name} {self.title}"

    class Meta:
        ordering = ["-publish", "-updated"]
        verbose_name = _("Blog")
        verbose_name_plural = _("Blogs")

    objects = BlogManager()


class Comment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="comments", verbose_name=_("User"),
    )
    name = models.CharField(
        max_length=20, null=True, 
        blank=True, verbose_name=_("Name"),
    )
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE,
        related_name="comments", verbose_name=_("content type"),
    )
    object_id = models.PositiveIntegerField(verbose_name=_("object id"),)
    content_object = GenericForeignKey("content_type", "object_id",)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE,
        related_name="children", null=True,
        blank=True, verbose_name=_("parent"),
    )
    category = models.CharField(max_length=300, blank=True, null=True)
    perspective = models.CharField(max_length=300, blank=True, null=True)
    body = models.TextField(verbose_name=_("Body"),)
    is_deleted = models.BooleanField(default=False)
    is_reviewed = models.BooleanField(default=False)
    has_perspective = models.BooleanField(default=False)
    create = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Create time"),
    )
    updated = models.DateTimeField(
        auto_now=True, verbose_name=_("Update time"),
    )

    def __str__(self):
        return self.user.phone

    objects = CommentManager()

    class Meta:
        ordering = [
            "-create", "-id",
        ]
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

