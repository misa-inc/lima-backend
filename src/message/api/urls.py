from django.urls import path
from .views import return_chat_messages,get_rooms,return_users_chats

urlpatterns = [
    path('users_chats/',return_users_chats , name="return_users_chats"),
    path('create/<username>/',return_chat_messages , name="return_chat_messages"),
    path('get_rooms/' ,get_rooms , name="get_rooms")
]