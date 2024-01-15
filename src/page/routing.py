from django.urls import re_path
from .consumers import PageConsumer


websocket_urlpatterns = [
    re_path(r'^ws/page/(?P<page_id>\w+)', PageConsumer.as_asgi()) 
]
