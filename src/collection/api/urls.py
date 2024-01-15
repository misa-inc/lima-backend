from django.urls import path
from .views import *


urlpatterns = [
    # collection VIEWS
    path('collection/create/', CreateCollectionView.as_view(), name='create_collection'),    
    path('collection/<str:name>/retrieve/', CollectionDetailView.as_view(), name='retrieve_collection'),
    path('collection/<str:name>/update/', CollectionUpdateView.as_view(), name='update_collection'),
    path('collection/<str:name>/delete/', CollectionDeleteView.as_view(), name='delete_collection'),
    path('user/creator/collection/', user_creator_collection, name='user_creator_collection'),
    path('user/collected/discussion/', user_collected_discussion, name='user_collected_discussion'),
    path('collect/discussion/', collect_discussion, name='collect_discussion'),
    path('user/collected/directory/', user_collected_directory, name='user_collected_directory'),
    path('collect/directory/', collect_directory, name='collect_directory'),
    path('user/collected/book/', user_collected_book, name='user_collected_book'),
    path('collect/book/', collect_book, name='collect_book'),
    path('user/collected/article/', user_collected_article, name='user_collected_article'),
    path('collect/article/', collect_article, name='collect_article'),
    path('user/collected/event/', user_collected_event, name='user_collected_event'),
    path('collect/event/', collect_event, name='collect_event'),
    path('user/collected/trivia/', user_collected_trivia, name='user_collected_trivia'),
    path('collect/trivia/', collect_trivia, name='collect_trivia'),
    path('user/collected/post/', user_collected_post, name='user_collected_post'),
    path('collect/post/', collect_post, name='collect_post'),
    path('users/collections/', ListCollectionsOfUser.as_view(), name='users_collections'),
    path('details/collection/', DetailCollectionOfUser, name='detail_collection'),
]
