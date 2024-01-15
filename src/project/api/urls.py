from django.urls import path
from .views import *


urlpatterns = [
    # Project VIEWS
    path('project/create/', CreateProjectView.as_view(), name='create_project'),    
    path('project/create/link/', CreateLinkView.as_view(), name='create_link'),
    path('project/create/rule/', CreateRuleView.as_view(), name='create_rule'),
    path('project/link/<int:id>/delete/', LinkDeleteView.as_view(), name='delete_link'),
    path('project/rule/<int:id>/delete/', RuleDeleteView.as_view(), name='delete_rule'),
    path('project/<str:name>/retrieve/', ProjectDetailView.as_view(), name='retrieve_project'),
    path('project/<str:name>/update/', ProjectUpdateView.as_view(), name='update_project'),
    path('project/<str:name>/delete/', ProjectDeleteView.as_view(), name='delete_project'),
    path('project/<str:name>/links/', ListLinksOfProject.as_view(), name='projects_links'),
    path('project/<str:name>/rules/', ListRulesOfProject.as_view(), name='projects_rules'),
    path("join/project/", join_project, name="join_project"),
    path('user/joined/project/', user_joined_project, name='user_joined_project'),
    path('user/<str:username>/creator/projects/', ListProjectsOfUser.as_view(), name='creator_projects'),
    path('user/moderator/projects/', ListProjectsUserIsModerator.as_view(), name='moderator_projects'),
    path('user/joined/projects/', ListProjectsUserIsJoined.as_view(), name='joined_projects'),
    path('project/<str:project_name>/posts/', ListPostsOfProject, name='projects_posts'),
    path('project/<str:project_name>/posts/<int:post_id>/', DetailPostOfProject.as_view(), name='projects_post_detail'),
]
