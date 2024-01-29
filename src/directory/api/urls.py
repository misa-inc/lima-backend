from django.urls import path
from .views import *


urlpatterns = [
    # Directory VIEWS
    path('directory/create/', CreateDirectoryView.as_view(), name='create_directory'),    
    path('directory/create/link/', CreateLinkView.as_view(), name='create_link'),
    path('directory/create/rule/', CreateRuleView.as_view(), name='create_rule'),
    path('directory/link/<int:id>/delete/', LinkDeleteView.as_view(), name='delete_link'),
    path('directory/rule/<int:id>/delete/', RuleDeleteView.as_view(), name='delete_rule'),
    path('directory/<str:name>/retrieve/', DirectoryDetailView.as_view(), name='retrieve_directory'),
    path('directory/<str:name>/update/', DirectoryUpdateView.as_view(), name='update_directory'),
    path('directory/<str:name>/delete/', DirectoryDeleteView.as_view(), name='delete_directory'),
    path('directory/<str:name>/links/', ListLinksOfDirectory.as_view(), name='directories_links'),
    path('directory/<str:name>/rules/', ListRulesOfDirectory.as_view(), name='directories_rules'),
    path("join/directory/", join_directory, name="join_directory"),
    path('user/joined/directory/', user_joined_directory, name='user_joined_directory'),
    path('add/remove/from/directory/', add_or_remove_from_directory, name='add_or_remove_from_directory'),
    path('user/<str:username>/creator/directories/', ListDirectoriesOfUser.as_view(), name='creator_directories'),
    path('user/moderator/directories/', ListDirectoriesUserIsModerator.as_view(), name='moderator_directories'),
    path('user/joined/directories/', ListDirectoriesUserIsJoined.as_view(), name='joined_directories'),
    path('directory/<str:directory_name>/posts/', ListPostsOfDirectory, name='directories_posts'),
    path('directory/<str:directory_name>/posts/<int:post_id>/', DetailPostOfDirectory.as_view(), name='directories_post_detail'),
]
