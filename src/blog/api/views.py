from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from directory.models import *
from page.models import *
from blog.models import Blog, Comment
from notifications.models import Notification
from account.models import Record
from .serializers import (
    BlogListSerializer,
    BlogCreateSerializer,
    BlogDetailUpdateDeleteSerializer,
    CommentListSerializer,
    CommentUpdateCreateSerializer,
)
from extensions.permissions import (
    IsSuperUserOrAuthor,
    IsSuperUserOrAuthorOrReadOnly,
)


class BlogList(ListAPIView):
    """
    get:
        Returns a list of all existing Blog.
    """

    serializer_class = BlogListSerializer
    filterset_fields = [
        "category", "special", "topics"
    ]
    search_fields = [
        "title", "summary",
        "author__first_name",
    ]
    ordering_fields = (
        "publish", "special",
    )

    def get_queryset(self):
        return Blog.objects.publish()


class BlogCreate(CreateAPIView):
    """
    post:
        Creates a new post instance. Returns created post data.

        parameters: [title,   body,    image,   summary, 
                    category, special, status, page, directory]
    """

    serializer_class = BlogCreateSerializer
    permission_classes = [IsSuperUserOrAuthor,]
    parser_classes = (FormParser, MultiPartParser)

    def create(self, request, *args, **kwargs):
        title = request.data.get("title")
        directory_id = request.data.get("directory_id")
        page_id = request.data.get("page_id")
        image = request.data.get("image")
        summary = request.data.get("summary")
        category = request.data.get("category")
        status = request.data.get("status")
        directory = get_object_or_404(Directory, id=directory_id)
        page = get_object_or_404(Page, id=page_id)
        author = request.user

        with transaction.atomic():
            if directory_id:
                blog = Blog.objects.create(
                    title=title,
                    image=image,
                    summary=summary,
                    category=category,
                    author=author,
                    directory=directory,
                    status=status,
                )
            elif page_id:
                blog = Blog.objects.create(
                    title=title,
                    image=image,
                    summary=summary,
                    category=category,
                    author=author,
                    page=page,
                    status=status,
                )  
            else:
                blog = Blog.objects.create(
                    title=title,
                    image=image,
                    summary=summary,
                    category=category,
                    author=author,
                    status=status,
                )      
        d = BlogCreateSerializer(blog).data
        return Response(d, status=status.HTTP_201_CREATED)


class BlogDetailUpdateDelete(RetrieveUpdateDestroyAPIView):
    """
    get:
        Returns the details of a post instance. Searches post using slug field.

    put:
        Updates an existing post. Returns updated post data.

        parameters: exclude = [user, create, updated, likes]

    delete:
        Delete an existing post.

        parameters = [slug]
    """

    serializer_class = BlogDetailUpdateDeleteSerializer
    permission_classes = (IsSuperUserOrAuthorOrReadOnly,)
    lookup_field = "slug"

    def get_queryset(self):
        return Blog.objects.publish()

    def perform_update(self, serializer):
        return serializer.save()


class LikeBlog(APIView):
    """
    get:
        Likes the desired blog.

        parameters = [pk]
    """

    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request, pk):
        user = request.user
        blog = get_object_or_404(Blog, pk=pk, status='p')

        if user in blog.likes.all():
            blog.likes.remove(user)
            
        else:
            blog.likes.add(user)
            Notification.objects.get_or_create(
                notification_type="L",
                comments=(f"@{user.username} likes your blog “{blog.title[:7]}...”"),
                to_user=blog.author,
                from_user=user,
                blog=blog
            )
        
        return Response(
            {
                "success" : "Your request was successful.",
            },
            status=200,
        )


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def user_likes_blog(request):
    if request.method == "POST":
        pk = request.data.get("pk")
        blog = get_object_or_404(Blog, id=pk)
        if request.user in blog.likes.all():
            likes = True
        else:
            likes = False
        return Response(
            {
                "likes": likes,
            },
            status=status.HTTP_200_OK,
        )


class CommentsList(APIView):
    """
    get:
        Returns the list of comments on a particular post.

        parameters = [pk]
    """

    def get(self, request, pk):
        blog = get_object_or_404(Blog, id=pk, status="p")
        query = Comment.objects.filter_by_instance(blog)
        serializer = CommentListSerializer(query, many=True)
        return Response(
            serializer.data, 
            status=status.HTTP_200_OK,
        )


class CommentCreate(APIView):
    """
    post:
        Create a comment instnace. Returns created comment data.

        parameters: [object_id, name, parent, body,]
    """

    permission_classes = [IsAuthenticated,]

    def post(self, request):
        serializer = CommentUpdateCreateSerializer(data=request.data)
        
        if serializer.is_valid():
            blog = get_object_or_404(Blog, pk=serializer.data.get('object_id'), status='p')
            comment_for_model = ContentType.objects.get_for_model(blog)
            comment = Comment.objects.create(
                user = request.user,
                name = serializer.data.get('name'),
                content_type = comment_for_model,
                object_id = Blog.id,
                parent_id = serializer.data.get('parent'),
                body = serializer.data.get('body'),
            )
            return Response(
                serializer.data, 
                status=status.HTTP_201_CREATED,
            )
        
        else:
            return Response(
                {
                  "error" : "The note you commented on is invalid.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
            

class CommentUpdateDelete(APIView):
    """
    put:
        Updates an existing comment. Returns updated comment data.

        parameters: [object_id, name, parent, body,]

    delete:
        Delete an existing comment.

        parameters: [pk]
    """

    permission_classes = [IsAuthenticated,]

    def put(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk, user=request.user)
        serializer = CommentUpdateCreateSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, 
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "error" : "The note you tried updating is invalid.",
                }, 
                status=status.HTTP_400_BAD_REQUEST,
            )


    def delete(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk, user=request.user)
        comment.delete()
        return Response(
            {
               "success" : "Successfully deleted the comment",
            },
            status=status.HTTP_204_NO_CONTENT,            
        )


class LikeComment(APIView):
    """
    get:
        Likes the desired comment.

        parameters = [pk]
    """

    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request, pk):
        user = request.user
        comment = get_object_or_404(Comment, pk=pk)

        if user in comment.likes.all():
            comment.likes.remove(user)

        else:
            comment.likes.add(user)
        
        return Response(
            {
                "success" : "Your request was successful.",
            },
            status=200,
        )


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def user_likes_comment(request):
    if request.method == "POST":
        pk = request.data.get("pk")
        comment = get_object_or_404(Comment, id=pk)
        if request.user in comment.likes.all():
            likes = True
        else:
            likes = False
        return Response(
            {
                "likes": likes,
            },
            status=status.HTTP_200_OK,
        )