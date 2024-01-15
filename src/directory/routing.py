from django.urls import re_path
from .consumers import DirectoryConsumer


websocket_urlpatterns = [
    re_path(r'^ws/directry/(?P<directry_id>\w+)', DirectoryConsumer.as_asgi()) 
]
