from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from blog.models import Blog, Comment
from .serializers import (
    BlogListSerializer,
    BlogCreateSerializer,
    BlogDetailUpdateDeleteSerializer,
    CommentListSerializer,
    CommentUpdateCreateSerializer,
)
from permissions import (
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
        "category", "special",
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
                    category, publish, special, status,]
    """

    serializer_class = BlogCreateSerializer
    permission_classes = [IsSuperUserOrAuthor,]
    queryset = Blog.objects.all()

    def perform_create(self, serializer):
        if not self.request.user.is_superuser:
            return serializer.save(
                author=self.request.user,
                status='d',
                special=False,
                )
        return serializer.save(author=self.request.user)


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
        if not self.request.user.is_superuser:
            return serializer.save(
                author=self.request.user,
                status='d',
                special=False,
                )
        return serializer.save()


class LikeBlog(APIView):
    """
    get:
        Likes the desired note.

        parameters = [pk]
    """

    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request, pk):
        user = request.user
        note = get_object_or_404(Blog, pk=pk, status='p')

        if user in note.likes.all():
            note.likes.remove(user)

        else:
            note.likes.add(user)
        
        return Response(
            {
                "success" : "Your request was successful.",
            },
            status=200,
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

