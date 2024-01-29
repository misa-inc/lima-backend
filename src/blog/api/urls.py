from django.urls import path

from .views import *

app_name = "api"

urlpatterns = [
    path("", BlogList.as_view(), name="list"),
    path("publication/create/", BlogCreate.as_view(), name="create"),
    path("publication/comments/<int:pk>/", CommentsList.as_view(), name="list"),
    path("publication/create/comment/", CommentCreate.as_view(), name="create"),
    path("publication/update-delete/comment/<int:pk>/", CommentUpdateDelete.as_view(), name="update-delete"),
    path("publication/<slug:slug>/", BlogDetailUpdateDelete.as_view(), name="detail"),
    path("publication/like/<int:pk>/", LikeBlog.as_view(), name="like_blog"),
    path("publication/like/<int:pk>/", LikeComment.as_view(), name="like_comment"),
    path("publication/likes/blog/", user_likes_blog, name="likes_blog"),
    path("publication/likes/comment/", user_likes_comment, name="likes_comment"),
]   
