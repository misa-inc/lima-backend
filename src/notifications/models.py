from django.db import models
from django.utils import timezone

from account.models import User
from post.models import Post, Comment
#TODO find more TYPE_CHOICES like Mentions (everytime you get mentioned in a post or comment)


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



class Notification(models.Model):

    TYPE_CHOICES = (
        ('C', 'comment'),#Comments From your comment*
        ('P', 'post'),#Comments From your post*
        ('RP', 'repost'),#reposts on your post*
        ('VP', 'vote_post'),#votes on your post*
        ('VC', 'vote_comment'),#votes on your comment*
        ('F', 'follow'),#when someone follows you*
        ('UF', 'unfollow'),#when someone unfollows you*
        ('M', 'Message'),#when someone messages you
    )

    from_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='create')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    comments = models.TextField(null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)
    user_has_seen = models.BooleanField(default=False)

    @property
    def created_time_ago(self):
        return time_ago(self.created)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return 'From: {} - To: {}'.format(self.from_user, self.to_user)
