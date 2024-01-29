from django.urls import path

from . import views

urlpatterns = [
    path('create-discussion', views.CreateDiscussionView, name='create-discussion'),
    path('discussion-detail/<int:id>', views.DiscussionDetailView, name='discussion-detail'),
    path('discussion-update/<int:id>', views.DiscussionUpdateView, name='discussion-update'),
    path('discussion-delete/<int:id>', views.DiscussionDeleteView, name='discussion-delete'),
    path('list-users-discussions', views.ListDiscussionsOfUsers, name='list-users-discussions'),
    path('user/creator/discussion', views.user_creator_discussion, name='user_creator_discussion'),
    path('user/joined/discussion', views.user_joined_discussion, name='user_joined_discussion'),
    path('join/discussion', views.join_discussion, name='join_discussion'),
    path('u/liked/discussion', views.user_liked_discussion, name='user_liked_discussion'),
    path('like/discussion', views.like_discussion, name='like_discussion'),
    path('user/blocked/in/discussion', views.user_blocked_in_discussion, name='user_blocked_in_discussion'),
    path('block/user/in/discussion', views.block_user_in_discussion, name='block_user_in_discussion'),
    path('added/moderator/in/discussion', views.added_moderator, name='added_moderator'),
    path('add/remove/moderator/in/discussion', views.add_remove_moderator, name='add_remove_moderator'),
    path('add/remove/project/in/discussion', views.add_remove_project, name='add_remove_project'),
    path('discussion/create-bot', views.CreateBotView, name='create-bot'),
    path('bot-detail/<int:id>', views.BotDetailView, name='bot-detail'),
    path('bot-update/<int:id>', views.BotUpdateView, name='bot-update'),
    path('bot-delete/<int:id>', views.BotDeleteView, name='bot-delete'),
    path('discussion/create-category', views.CreateCategoryView, name='create-category'),
    path('category-detail/<int:id>', views.CategoryDetailView, name='category-detail'),
    path('category-update/<int:id>', views.CategoryUpdateView, name='category-update'),
    path('category-delete/<int:id>', views.CategoryDeleteView, name='category-delete'),
    path('getMe', views.getMe, name='get_me'),
    path('list_discussions_chats/<int:id>', views.ListChatsOfDiscussion, name='list_discussions_chats'),
    path('chat-delete', views.ChatDeleteView, name='chat-delete')
]
