from django.urls import path

from .views import (
    BlogList,
    BlogCreate,
    BlogDetailUpdateDelete,
    LikeBlog,
    CommentsList,
    CommentCreate,
    CommentUpdateDelete,
)

app_name = "api"

urlpatterns = [
    path("", BlogList.as_view(), name="list"),
    path("create/", BlogCreate.as_view(), name="create"),
    path("comments/<int:pk>/", CommentsList.as_view(), name="list"),
    path("create/comment/", CommentCreate.as_view(), name="create"),
    path("update-delete/comment/<int:pk>/", CommentUpdateDelete.as_view(), name="update-delete"),
    path("<slug:slug>/", BlogDetailUpdateDelete.as_view(), name="detail"),
    path("like/<int:pk>/", LikeBlog.as_view(), name="like"),
]   
