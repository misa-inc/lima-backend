from project.consumers import TimelineConsumer
from django.urls import re_path, path 
from message.consumers import MessageConsumer
from discussion.consumer import ChatConsumer, NotifConsumer

from django.conf.urls import url  


websocket_urlpatterns = [
    re_path(r'^ws/timeline/(?P<user_id>\w+)', TimelineConsumer.as_asgi()),
    url(r'ws/message/(?P<username>\w+)', MessageConsumer.as_asgi()),
    path('ws/chat/<str:discussion_code>/', ChatConsumer.as_asgi()) ,
    path('ws/notif/', NotifConsumer.as_asgi())   
]
