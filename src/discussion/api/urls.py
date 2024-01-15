from django.urls import path

from . import views

urlpatterns = [
    path('create-discussion', views.CreateDiscussionView, name='create-discussion'),
    path('discussion-detail/<str:discussion_name>', views.DiscussionDetailView, name='discussion-detail'),
    path('discussion-update/<str:discussion_name>', views.DiscussionUpdateView, name='discussion-update'),
    path('discussion-delete/<str:discussion_name>', views.DiscussionDeleteView, name='discussion-delete'),
    path('list-users-discussions', views.ListDiscussionsOfUsers, name='list-users-discussions'),
    path('u/creator/discussion', views.user_creator_discussion, name='user_creator_discussion'),
    path('u/joined/discussion', views.user_joined_discussion, name='user_joined_discussion'),
    path('join/discussion', views.join_discussion, name='join_discussion'),
    path('u/blocked/in/discussion', views.user_blocked_in_discussion, name='user_blocked_in_discussion'),
    path('block/user/in/discussion', views.block_user_in_discussion, name='block_user_in_discussion'),
    path('create-bot', views.CreateBotView, name='create-bot'),
    path('bot-detail/<str:discussion_name>', views.BotDetailView, name='bot-detail'),
    path('bot-update/<str:discussion_name>', views.BotUpdateView, name='bot-update'),
    path('bot-delete/<str:discussion_name>', views.BotDeleteView, name='bot-delete'),
    path('getMe', views.getMe, name='get_me'),
    path('list_discussions_chats/<int:id>', views.ListChatsOfDiscussion, name='list_discussions_chats'),
    path('chat-delete', views.ChatDeleteView, name='chat-delete')
]
