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
# TODO Add more details to trivias, comments


def link_to(instance, filename):
    return "links/{0}/{1}".format(instance.title, filename)


def trivia_to(instance, filename):
    return "trivias/{0}/{1}".format(instance.slug, filename)


def trivia_to(instance, filename):
    return "trivias/{0}/{1}".format(instance.slug, filename)


def trivia_for(instance, filename):
    return "trivias/{0}/{1}".format(instance.slug, filename)


def get_perm(codename):
    return Permission.objects.get(content_type__app_label="pyramid", codename=codename)


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

def add_post_util(instance):
    now = date.today()
    if not instance.month:
        instance.subscriber_count =+ 1
        instance.day = now.day
        instance.month = month[now.month]
        instance.year = now.year
        instance.save()

        
def add_post_utils(instance):    
    creator = instance.creator
    instance.subscribers.add(creator)
    instance.moderators.add(creator)
    instance.save()        


class Text(models.Model):
    text = models.TextField(blank=True)
    last_modified = models.DateTimeField(auto_now=True)


class DeletedUser(object):
    username = "[deleted]"

    def get_username(self):
        return self.username


#TODO Add the all different types of trivias [Live + Quizzes] is left to be added
class Trivia(models.Model):
    attachment = models.ImageField(
        upload_to=trivia_to, blank=True, null=True, max_length=100000
    )
    video = models.FileField(
        upload_to=trivia_to, blank=True, null=True, max_length=1000000
    )
    title = models.CharField(max_length=1000, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    link = models.URLField(blank=True, null=True, max_length=2000)
    description = models.TextField(blank=True, null=True)
    trivia_type = models.CharField(max_length=300, blank=True, null=True)
    category = models.CharField(max_length=300, blank=True, null=True)
    perspective = models.CharField(max_length=300, blank=True, null=True)
    parent = models.ForeignKey(
        "self", blank=True, null=True, on_delete=models.CASCADE, related_name="alt"
    )
    author = models.ForeignKey(
        'account.User', on_delete=models.CASCADE, related_name="trivia_author"
    )
    report = models.ManyToManyField(
        'account.User', related_name="trivia_report", blank=True, default=None
    )
    saved = models.ManyToManyField(
        'account.User', related_name="trivia_saved", blank=True, default=None
    )
    share_count = models.IntegerField(blank=True, null=True, default=0)
    saved_count = models.IntegerField(blank=True, null=True, default=0)
    report_count = models.IntegerField(blank=True, null=True, default=0)
    is_deleted = models.BooleanField(default=False)
    is_reviewed = models.BooleanField(default=False)
    has_perspective = models.BooleanField(default=False)
    voters = models.ManyToManyField(
        'account.User',
        related_name="trivia_voters",
    )
    votes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    slug = models.SlugField(blank=True, null=False, max_length=1000)

    def get_author(self):
        if self.is_deleted:
            return DeletedUser()
        return self.author

    @property
    def top_comments(self):
        return self.comment_set.order_by("votes")

    @property
    def new_comments(self):
        return self.comment_set.order_by("created")

    @property
    def old_comments(self):
        return self.comment_set.order_by("-created")

    @property
    def created_time_ago(self):
        return time_ago(self.created)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.trivia_type)
        new_record = self.pk is None
        with transaction.atomic():
            super(Trivia, self).save(*args, **kwargs)
            if new_record:
                Vote.objects.create(voter=self.author, value=1, trivia=self)
                assign_perm("trivia.change_trivia", self.author, self)
                assign_perm("trivia.delete_trivia", self.author, self)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return self.slug


class Quiz(models.Model):
    author = models.ForeignKey(
        'account.User', on_delete=models.CASCADE, related_name="quiz_author"
    )
    trivia = models.ForeignKey(Trivia, on_delete=models.CASCADE, null=True, blank=True)
    category = models.CharField(max_length=300, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    answer_one = models.TextField(blank=True, null=True)
    answer_two = models.TextField(blank=True, null=True)
    answer_three = models.TextField(blank=True, null=True)
    answer_four = models.TextField(blank=True, null=True)
    answer_five = models.TextField(blank=True, null=True)
    answer_is = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    active_for = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_date",)

    def __str__(self):
        return self.title


class Comment(models.Model):
    trivia = models.ForeignKey(Trivia, on_delete=models.CASCADE, null=True, blank=True)
    author = models.ForeignKey(
        'account.User', on_delete=models.CASCADE, related_name="trivia_comment_author"
    )
    parent_comment = models.ForeignKey(
        "self", null=True, on_delete=models.CASCADE, blank=True
    )
    report = models.ManyToManyField(
        'account.User', related_name="trivia_comment_report", blank=True, default=None
    )
    saved = models.ManyToManyField(
        'account.User', related_name="trivia_comment_saved", blank=True, default=None
    )
    perspective = models.CharField(max_length=300, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    text = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    has_perspective = models.BooleanField(default=False)
    saved_count = models.IntegerField(blank=True, null=True, default=0)
    report_count = models.IntegerField(blank=True, null=True, default=0)
    share_count = models.IntegerField(blank=True, null=True, default=0)
    voters = models.ManyToManyField(
        'account.User',
        related_name="trivia_comment_voters",
    )
    votes = models.IntegerField(default=0)

    def get_author(self):
        if self.is_deleted:
            return DeletedUser()
        return self.author

    @property
    def saved_count(self):
        return self.saved.all().count()

    @property
    def report_count(self):
        return self.report.all().count()

    @property
    def child_comments(self):
        return self.comment_set.all().order_by("-votes", "created")

    @property
    def created_time_ago(self):
        return time_ago(self.created)

    def save(self, *args, **kwargs):
        new_record = self.pk is None
        with transaction.atomic():
            super(Comment, self).save(*args, **kwargs)
            if new_record:
                Vote.objects.create(voter=self.author, value=1, comment=self)
                assign_perm("trivia.change_comment", self.author, self)
                assign_perm("trivia.delete_comment", self.author, self)

    def __str__(self):
        if len(self.text) < 20:
            return self.text
        return self.text[:20] + "..."


class VoteManager(models.Manager):
    def create(self, voter, value, trivia=None, comment=None):
        vote = self.model(
            voter=voter,
            value=value,
            is_trivia=bool(trivia),
            is_comment=bool(comment),
            trivia=trivia,
            comment=comment,
        )
        vote.save()
        return vote


class Vote(models.Model):
    voter = models.ForeignKey('account.User', related_name="trivia_voter", on_delete=models.CASCADE)
    value = models.IntegerField()  # should be 1
    is_trivia = models.BooleanField()
    is_comment = models.BooleanField()
    trivia = models.ForeignKey(Trivia, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, null=True, blank=True
    )
    objects = VoteManager()

    def validate(self):
        if self.value != 1:
            raise FieldError("value must be in 1")
        if self.trivia is None and self.comment is None:
            raise FieldError("trivia and comment cannot both be null")
        if self.trivia and self.comment:
            raise FieldError("cannot submit vote for both trivia and comment")
        if self.pk is None and self.trivia and self.voter in self.trivia.voters.all():
            raise FieldError("voter has already voted on this trivia")
        if self.pk is None and self.comment and self.voter in self.comment.voters.all():
            raise FieldError("voter has already voted on this comment")
        return True

    def save(self, *args, **kwargs):
        self.validate()
        with transaction.atomic():
            super(Vote, self).save(*args, **kwargs)
            if self.comment:
                value__sum = self.comment.vote_set.aggregate(Sum("value"))
                self.comment.votes = value__sum["value__sum"]
                self.comment.save()  
            if self.trivia:
                value__sum = self.trivia.vote_set.aggregate(Sum("value"))
                self.trivia.votes = value__sum["value__sum"]
                self.trivia.save()

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            if self.comment:
                self.comment.votes -= self.value
                self.comment.save()   
            if self.trivia:
                self.trivia.votes -= self.value
                self.trivia.save()
            super(Vote, self).delete(*args, **kwargs)
