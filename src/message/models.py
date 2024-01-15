from django.db import models
from datetime import date, datetime
from django.utils import timezone
from extensions.utils import MONTH as month
from account.models import User
from django.db.models import Q



def file_to(instance, filename):
    return "message/{0}/{1}".format(instance.sender.username, filename)


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


class MessageManager(models.Manager):
    def by_room(self, room):
        messages = Message.objects.filter(room=room).order_by("-created_at")
        return messages


class PrivateChatManager(models.Manager):
    def create_room_if_none(self,u1,u2):
        has_room = PrivateChat.objects.filter(Q(user1=u1 ,user2=u2)| Q(user1=u2,user2=u1)).first()
        if not has_room:
            print('not found so creating one ')
            PrivateChat.objects.create(user1=u1,user2=u2)
        return has_room  


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PrivateChat(BaseModel):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user1")
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user2")
    connected_users = models.ManyToManyField(
        User, blank=True, related_name="connected_users")
    is_active = models.BooleanField(default=False)
    objects = PrivateChatManager()


    def connect(self,user):
        is_added = False
        if not user in self.connected_users.all():
            self.connected_users.add(user)
            is_added = True
        return is_added
    
    def disconnect(self,user):
        is_removed = False
        if not user in self.connected_users.all():
            self.connected_users.remove(user)
            is_removed = True
        return is_removed
    
    def last_msg(self):
        return self.message_set.all().last()
    
    def __str__(self) -> str:
        return f'Chat : {self.user1} - {self.user2}'
    

class Message(BaseModel):
    room = models.ForeignKey(PrivateChat, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to=file_to, blank=True, null=True, max_length=1000000)
    text = models.TextField(blank=False, null=False)
    created = models.DateTimeField(default=timezone.now)
    day = models.CharField(max_length=3, null=True, blank=True)
    month = models.CharField(max_length=15, null=True, blank=True)
    year = models.CharField(max_length=7, null=True, blank=True)
    time = models.CharField(max_length=15, null=True, blank=True)
    objects = MessageManager()

    def __str__(self) -> str:
        return f'From <Room - {self.room}>'
    
    def save(self, *args, **kwargs):
        time_n_day_ago(self)
        super().save(*args, **kwargs)