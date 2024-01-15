from django.urls import path
from .views import ListPagesUserIsJoined, ListPagesUserIsModerator, RuleDeleteView, LinkDeleteView, CreateRuleView, CreateLinkView, ListRulesOfPage, ListLinksOfPage, user_joined_page, PageDeleteView, PageUpdateView, PageDetailView, CreatePageView, ListPagesOfUser, join_page, ListPostsOfPage, DetailPostOfPage


urlpatterns = [
    # Page VIEWS
    path('page/create/', CreatePageView.as_view(), name='create_page'),    
    path('page/create/link/', CreateLinkView.as_view(), name='create_link'),
    path('page/create/rule/', CreateRuleView.as_view(), name='create_rule'),
    path('page/link/<int:id>/delete/', LinkDeleteView.as_view(), name='delete_link'),
    path('page/rule/<int:id>/delete/', RuleDeleteView.as_view(), name='delete_rule'),
    path('page/<str:name>/retrieve/', PageDetailView.as_view(), name='retrieve_page'),
    path('page/<str:name>/update/', PageUpdateView.as_view(), name='update_page'),
    path('page/<str:name>/delete/', PageDeleteView.as_view(), name='delete_page'),
    path('page/<str:name>/links/', ListLinksOfPage.as_view(), name='pages_links'),
    path('page/<str:name>/rules/', ListRulesOfPage.as_view(), name='pages_rules'),
    path("join/page/", join_page, name="join_page"),
    path('user/joined/page/', user_joined_page, name='user_joined_page'),
    path('user/<str:username>/creator/pages/', ListPagesOfUser.as_view(), name='creator_pages'),
    path('user/moderator/pages/', ListPagesUserIsModerator.as_view(), name='moderator_pages'),
    path('user/joined/pages/', ListPagesUserIsJoined.as_view(), name='joined_pages'),
    path('page/<str:page_name>/posts/', ListPostsOfPage, name='pages_posts'),
    path('page/<str:page_name>/posts/<int:post_id>/', DetailPostOfPage.as_view(), name='pages_post_detail'),
]
