import jwt
import os
import requests
import random
import string
import re
 
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponsePermanentRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.conf import settings
from django.contrib import auth
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import (
    smart_str,
    force_str,
    smart_bytes,
    DjangoUnicodeDecodeError,
)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.db import transaction
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.views import View
from django.views.generic import *
from django.db.models import Count

from .serializers import *
from post.models import *
from account.models import Record
from extensions.pagination import CustomPagination
from notifications.models import Notification

from rest_framework import viewsets, exceptions, generics
from rest_framework.response import Response
from rest_framework.generics import *
from rest_framework.permissions import *
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import (
    RetrieveUpdateAPIView,
    CreateAPIView,
    ListAPIView,
    UpdateAPIView,
    RetrieveAPIView,
    DestroyAPIView,
    RetrieveUpdateDestroyAPIView,
    ListCreateAPIView
)

# TODO Notifications automatically from the group you are part of, on comments on your comments



@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def RePostView(request):
    text = request.data.get("text")
    directory_id = request.data.get("directory_id")
    page_id = request.data.get("page_id")
    p_id = request.data.get("p_id")
    directory = get_object_or_404(Directory, id=directory_id)
    page = get_object_or_404(Page, id=page_id)

    try:
        post = get_object_or_404(Post, id=p_id)
    except:
        return Response({"error": "The post you tried to repost was not found",}, status=status.HTTP_200_OK)
    if post.author == request.user:
        return Response({"error": "Can't repost your own post",}, status=status.HTTP_200_OK)
    # try:
    parent_post = Post.objects.filter(parent=post, author=request.user)
    if parent_post.exists():
        return Response({"error": "Already reposted !",}, status=status.HTTP_200_OK)
    else:
        with transaction.atomic():
            if directory_id:
                re_post = Post.objects.create(
                    text=text,
                    author=request.user,
                    parent=post,
                    directory=directory,
                    is_repost=True,
                )
            elif page_id:
                re_post = Post.objects.create(
                    text=text,
                    author=request.user,
                    parent=post,
                    page=page,
                    is_repost=True,
                )
            else:
                re_post = Post.objects.create(
                    text=text,
                    author=request.user,
                    parent=post,
                    is_repost=True,
                )        
            post.reposts = post.reposts + 1
            post.save()
            Notification.objects.get_or_create(
                notification_type="RP",
                post=re_post,
                comments=(
                    f"@{request.user.username} reposted your post"
                ),
                to_user=post.author,
                from_user=request.user,
            )
        return Response({"success": "The repost was created successfully"}, status=status.HTTP_201_CREATED)


class CreatePostView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (FormParser, MultiPartParser)
    serializer_class = PostSerializer

    def create(self, request, *args, **kwargs):
        title = request.data.get("title")
        directory_id = request.data.get("directory_id")
        page_id = request.data.get("page_id")
        is_walk_through = request.data.get("is_walk_through")
        attachment = request.data.get("attachment")
        video = request.data.get("video")
        link = request.data.get("link")
        text = request.data.get("text")
        post_type = request.data.get("post_type")
        post_status = request.data.get("post_status")
        directory = get_object_or_404(Directory, id=directory_id)
        page = get_object_or_404(Page, id=page_id)
        author = request.user

        with transaction.atomic():
            if directory_id and is_walk_through:
                post = Post.objects.create(
                    title=title,
                    attachment=attachment,
                    video=video,
                    link=link,
                    text=text,
                    author=author,
                    directory=directory,
                    is_walk_through=True,
                    post_type=post_type,
                    post_status=post_status,
                )
            elif directory_id:
                post = Post.objects.create(
                    title=title,
                    attachment=attachment,
                    video=video,
                    link=link,
                    text=text,
                    author=author,
                    directory=directory,
                    post_type=post_type,
                    post_status=post_status,
                )    
            elif page_id:
                post = Post.objects.create(
                    title=title,
                    attachment=attachment,
                    video=video,
                    link=link,
                    text=text,
                    author=author,
                    page=page,
                    post_type=post_type,
                    post_status=post_status,
                )  
            else:
                post = Post.objects.create(
                    title=title,
                    attachment=attachment,
                    video=video,
                    link=link,
                    text=text,
                    author=author,
                    post_type=post_type,
                    post_status=post_status,
                )      
        d = PostSerializer(post).data
        return Response(d, status=status.HTTP_201_CREATED)


class PostUpdateView(UpdateAPIView):
    lookup_field = "id"
    permission_classes = (IsAuthenticated,)
    parser_classes = (FormParser, MultiPartParser)
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class PostDeleteView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self,request):
        data = request.data
        post = get_object_or_404(Post,id=data.get('post_id'))
        if post.author == request.user:
            post.delete()
            return Response({"success": "Post has been deleted"})


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def ListPostsOfUser(request, username):
    post = Post.objects.filter(
            author__username=username, is_reviewed=True, is_deleted=False
        )
    paginator = CustomPagination()
    result_page = paginator.paginate_queryset(post,request)

    serializer = PostSerializer_detailed(result_page, many=True, context={'request': request})
    return paginator.get_paginated_response({'data':serializer.data})    
    

class DetailPostOfUser(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Post.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return PostSerializer_detailed
        return PostSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        conditions = {
            "author__username": self.kwargs["username"],
            "id": self.kwargs["post_id"],
        }
        return get_object_or_404(queryset, **conditions)

    def put(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def ListPostsOfDirectory(request, directory_name):
    post = Post.objects.filter(
            directory__name=directory_name, is_reviewed=True, is_deleted=False
        )
    paginator = CustomPagination()
    result_page = paginator.paginate_queryset(post,request)

    serializer = PostSerializer_detailed(result_page, many=True, context={'request': request})
    return paginator.get_paginated_response({'data':serializer.data})     
    

class DetailPostOfDirectory(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Post.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return PostSerializer_detailed
        return PostSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        conditions = {"directory__name": self.kwargs["directory_name"], "id": self.kwargs["post_id"]}
        return get_object_or_404(queryset, **conditions)

    def put(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def user_saved_post(request):
    if request.method == "POST":
        pk = request.data.get("pk")
        post = get_object_or_404(Post, id=pk)
        if request.user in post.saved.all():
            saved = True
        else:
            saved = False
        return Response(
            {
                "saved": saved,
            },
            status=status.HTTP_200_OK,
        )


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def save_post(request):
    if request.method == "POST":
        pk = request.data.get("pk")
        post = get_object_or_404(Post, id=pk)
        if request.user in post.saved.all():
            saved = False
            post.saved.remove(request.user)
            post.saved_count = post.saved_count - 1
            post.save()
        else:
            saved = True
            post.saved.add(request.user)
            post.saved_count = post.saved_count + 1
            post.save()
        return Response(
            {
                "saved": saved,
            },
            status=status.HTTP_201_CREATED,
        )


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def user_reported_post(request):
    if request.method == "POST":
        pk = request.data.get("pk")
        post = get_object_or_404(Post, id=pk)
        if request.user in post.report.all():
            report = True
        else:
            report = False
        return Response(
            {
                "report": report,
            },
            status=status.HTTP_200_OK,
        )


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def report_post(request):
    if request.method == "POST":
        pk = request.data.get("pk")
        post = get_object_or_404(Post, id=pk)
        if request.user in post.report.all():
            report = False
            post.report.remove(request.user)
            post.report_count = post.report_count - 1
            post.save()
        else:
            report = True
            post.report.add(request.user)
            post.report_count = post.report_count + 1
            post.save()
        return Response(
            {
                "report": report,
            },
            status=status.HTTP_201_CREATED,
        )


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def VoteOnPost(request):
    if request.method == "POST":
        voter = request.user
        post_id = request.data.get("post_id")
        value = request.data.get("value")
        post = get_object_or_404(Post, id=post_id)

        if value == 1:
            Notification.objects.get_or_create(
                notification_type="L",
                post=post,
                comments=(
                    f"@{voter.username} likes your post “{post.text[:7]}...”"
                ),
                to_user=post.author,
                from_user=voter,
            )
        try:
            vote = Vote.objects.get(voter=voter, post=post)
        except Vote.DoesNotExist:
            vote = Vote.objects.create(voter, value, post=post)
        else:
            if value in [-1, 1]:
                vote.value = value
                vote.save()
            elif value == 0:
                vote.delete()

        return Response(
            {"success": PostSerializer(get_object_or_404(Post, id=post_id)).data},
                status=status.HTTP_201_CREATED,
        )        
        


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def user_voted_post(request):
    if request.method == "POST":
        voter = request.user
        pk = request.data.get("pk")
        post = get_object_or_404(Post, id=pk)
        if voter in post.voters.all():
            voted = True
            vote = Vote.objects.get(voter=voter, post=post).value
        else:
            voted = False
            vote = 0
        return Response(
            {
                "voted": voted,
                "vote": vote,
            },
            status=status.HTTP_200_OK,
        )


class CreateCommentView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)
    serializer_class = CommentSerializer

    def create(self, request, *args, **kwargs):
        author = request.user
        post_id = request.data.get("post_id")
        text = request.data.get("text")
        parent_comment_id = request.data.get("parent_comment_id")
        post = get_object_or_404(Post, id=post_id)

        with transaction.atomic():
            comment = Comment.objects.create(
                post=post,
                author=author,
                parent_comment=parent_comment_id
                and Comment.objects.get(pk=parent_comment_id),
                text=text,
            )
            post.comments = post.comments + 1
            post.save()
        if post.post_type == "qna" or "poll":
            Record.objects.get_or_create(
                user=author,
                aura="6",
                posts=post,
                time="3",
                type="minor",
                status="closed",
                description=(f"You earned aura by engaging on this post “{post.text[:7]}...”")
            )
            author.total_aura = author.total_aura + 6
            author.save()    
        if parent_comment_id and Comment.objects.get(pk=parent_comment_id):
            Notification.objects.get_or_create(
                notification_type="C",
                comment=Comment.objects.get(pk=parent_comment_id),
                comments=(
                    f"@{author.username} replied to your comment"
                ),
                to_user=Comment.objects.get(pk=parent_comment_id).author,
                from_user=author,
            )
        else:
            Notification.objects.get_or_create(
                notification_type="C",
                post=post,
                comments=(
                    f"@{author.username} commented on your post"
                ),
                to_user=post.author,
                from_user=author,
            )

        d = CommentSerializer(comment).data
        return Response(d, status=status.HTTP_201_CREATED)


class CommentUpdateView(UpdateAPIView):
    lookup_field = "id"
    permission_classes = (IsAuthenticated,)
    parser_classes = (FormParser, MultiPartParser)
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()


class CommentDeleteView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self,request):
        data = request.data
        comment = get_object_or_404(Comment,id=data.get('comment_id'))
        if comment.author == request.user:
            comment.delete()
            return Response({"success": "Comment has been deleted successfully"})

    
@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def VoteOnComment(request):
    if request.method == "POST":
        voter = request.user
        comment_id = request.data.get("comment_id")
        value = request.data.get("value")
        comment = get_object_or_404(Comment, id=comment_id)

        if value == 1:
            Notification.objects.get_or_create(
                notification_type="L",
                comment=comment,
                comments=(
                    f"@{voter.username} likes your comment “{comment.text[:7]}...”"
                ),
                to_user=comment.author,
                from_user=voter,
            )
        try:
            vote = Vote.objects.get(voter=voter, comment=comment)
        except Vote.DoesNotExist:
            vote = Vote.objects.create(voter, value, comment=comment)
        else:
            if value in [-1, 1]:
                vote.value = value
                vote.save()
            elif value == 0:
                vote.delete()

        return Response(
            {
                "success": CommentSerializer(
                    get_object_or_404(Comment, id=comment_id)
                ).data
            },
            status=status.HTTP_201_CREATED,
        )


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def user_voted_comment(request):
    if request.method == "POST":
        voter = request.user
        pk = request.data.get("pk")
        comment = get_object_or_404(Comment, id=pk)
        if voter in comment.voters.all():
            voted = True
            vote = Vote.objects.get(voter=voter, comment=comment).value
        else:
            voted = False
            vote = 0
        return Response(
            {
                "voted": voted,
                "vote": vote,
            },
            status=status.HTTP_200_OK,
        )


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def user_saved_comment(request):
    if request.method == "POST":
        pk = request.data.get("pk")
        comment = get_object_or_404(Comment, id=pk)
        if request.user in comment.saved.all():
            saved = True
        else:
            saved = False
        return Response(
            {
                "saved": saved,
            },
            status=status.HTTP_200_OK,
        )


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def user_reported_comment(request):
    if request.method == "POST":
        pk = request.data.get("pk")
        comment = get_object_or_404(Comment, id=pk)
        if request.user in comment.report.all():
            report = True
        else:
            report = False
        return Response(
            {
                "report": report,
            },
            status=status.HTTP_200_OK,
        )


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def save_comment(request):
    if request.method == "POST":
        pk = request.data.get("pk")
        comment = get_object_or_404(Comment, id=pk)
        if request.user in comment.saved.all():
            saved = False
            comment.saved.remove(request.user)
        else:
            saved = True
            comment.saved.add(request.user)
        return Response(
            {
                "saved": saved,
            },
            status=status.HTTP_201_CREATED,
        )


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def report_comment(request):
    if request.method == "POST":
        pk = request.data.get("pk")
        comment = get_object_or_404(Comment, id=pk)
        if request.user in comment.report.all():
            report = False
            comment.report.remove(request.user)
        else:
            report = True
            comment.report.add(request.user)
        return Response(
            {
                "report": report,
            },
            status=status.HTTP_201_CREATED,
        )


class ListNewCommentsOfPost(ListAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CommentSerializer_detailed
        if self.request.method == "POST":
            return CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(
            post__id=self.kwargs["p_id"]
        ).order_by("-created")


class ListOldCommentsOfPost(ListAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CommentSerializer_detailed
        if self.request.method == "POST":
            return CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(
            post__id=self.kwargs["p_id"]
        ).order_by("created")


class ListPopularCommentsOfPost(ListAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CommentSerializer_detailed
        if self.request.method == "POST":
            return CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(
            post__id=self.kwargs["p_id"]
        ).order_by("votes")


class DetailCommentsOfPost(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Comment.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CommentSerializer_detailed
        return CommentSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        conditions = {
            "post__id": self.kwargs["p_id"],
            "id": self.kwargs["c_id"],
        }
        return get_object_or_404(queryset, **conditions)

    def put(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)


class ListCommentsOfUser(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CommentSerializer_detailed
        if self.request.method == "POST":
            return CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(
            author__username=self.kwargs["username"]
        ).order_by("-created")


class DetailCommentsOfUser(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Comment.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CommentSerializer_detailed
        return CommentSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        conditions = {
            "author__username": self.kwargs["username"],
            "id": self.kwargs["c_id"],
        }
        return get_object_or_404(queryset, **conditions)

    def put(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)


class CreateAnswerView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)
    serializer_class = AnswerSerializer

    def create(self, request, *args, **kwargs):
        author = request.user
        post_id = request.data.get("post_id")
        text = request.data.get("text")
        parent_answer_id = request.data.get("parent_answer_id")
        post = get_object_or_404(Post, id=post_id)

        with transaction.atomic():
            answer = Answer.objects.create(
                post=post,
                author=author,
                parent_answer=parent_answer_id
                and Answer.objects.get(pk=parent_answer_id),
                text=text,
            )
            post.answers = post.answers + 1
            post.save()
            Record.objects.get_or_create(
                user=author,
                aura="6",
                posts=post,
                time="3",
                type="minor",
                status="closed",
                description=(f"You earned 6 aura by engaging on this post “{post.text[:7]}...”")
            )
            author.total_aura = author.total_aura + 6
            author.save()
        if parent_answer_id and Answer.objects.get(pk=parent_answer_id):
            Notification.objects.get_or_create(
                notification_type="C",
                answer=Answer.objects.get(pk=parent_answer_id),
                comments=(
                    f"@{author.username} replied to your question"
                ),
                to_user=Answer.objects.get(pk=parent_answer_id).author,
                from_user=author,
            )
        else:
            Notification.objects.get_or_create(
                notification_type="C",
                post=post,
                comments=(
                    f"@{author.username} replied to your question"
                ),
                to_user=post.author,
                from_user=author,
            )

        d = AnswerSerializer(answer).data
        return Response(d, status=status.HTTP_201_CREATED)


class AnswerUpdateView(UpdateAPIView):
    lookup_field = "id"
    permission_classes = (IsAuthenticated,)
    parser_classes = (FormParser, MultiPartParser)
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()


class AnswerDeleteView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self,request):
        data = request.data
        answer = get_object_or_404(Answer,id=data.get('Answer_id'))
        if answer.author == request.user:
            answer.delete()
            return Response({"success": "Answer has been deleted successfully"})

    
@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def VoteOnAnswer(request):
    if request.method == "POST":
        voter = request.user
        answer_id = request.data.get("answer_id")
        value = request.data.get("value")
        answer = get_object_or_404(Answer, id=answer_id)

        if value == 1:
            Notification.objects.get_or_create(
                notification_type="L",
                answer=answer,
                comments=(
                    f"@{voter.username} likes your answer “{answer.body[:7]}...”"
                ),
                to_user=answer.author,
                from_user=voter,
            )
        try:
            vote = Vote.objects.get(voter=voter, answer=answer)
        except Vote.DoesNotExist:
            vote = Vote.objects.create(voter, value, answer=answer)
        else:
            if value == 1:
                vote.value = value
                vote.save()
            elif value == 0:
                vote.delete()

        return Response(
            {
                "success": AnswerSerializer(
                    get_object_or_404(Answer, id=answer_id)
                ).data
            },
            status=status.HTTP_201_CREATED,
        )


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def user_voted_answer(request):
    if request.method == "POST":
        voter = request.user
        pk = request.data.get("pk")
        answer = get_object_or_404(Answer, id=pk)
        if voter in answer.voters.all():
            voted = True
            vote = Vote.objects.get(voter=voter, answer=answer).value
        else:
            voted = False
            vote = 0
        return Response(
            {
                "voted": voted,
                "vote": vote,
            },
            status=status.HTTP_200_OK,
        )


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def user_saved_answer(request):
    if request.method == "POST":
        pk = request.data.get("pk")
        answer = get_object_or_404(Answer, id=pk)
        if request.user in answer.saved.all():
            saved = True
        else:
            saved = False
        return Response(
            {
                "saved": saved,
            },
            status=status.HTTP_200_OK,
        )


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def user_reported_answer(request):
    if request.method == "POST":
        pk = request.data.get("pk")
        answer = get_object_or_404(Answer, id=pk)
        if request.user in answer.report.all():
            report = True
        else:
            report = False
        return Response(
            {
                "report": report,
            },
            status=status.HTTP_200_OK,
        )


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def save_answer(request):
    if request.method == "POST":
        pk = request.data.get("pk")
        answer = get_object_or_404(Answer, id=pk)
        if request.user in answer.saved.all():
            saved = False
            answer.saved.remove(request.user)
        else:
            saved = True
            answer.saved.add(request.user)
        return Response(
            {
                "saved": saved,
            },
            status=status.HTTP_201_CREATED,
        )


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def report_answer(request):
    if request.method == "POST":
        pk = request.data.get("pk")
        answer = get_object_or_404(Answer, id=pk)
        if request.user in answer.report.all():
            report = False
            answer.report.remove(request.user)
        else:
            report = True
            answer.report.add(request.user)
        return Response(
            {
                "report": report,
            },
            status=status.HTTP_201_CREATED,
        )


class ListNewAnswersOfPost(ListAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.request.method == "GET":
            return AnswerSerializer_detailed
        if self.request.method == "POST":
            return AnswerSerializer

    def get_queryset(self):
        return Answer.objects.filter(
            post__id=self.kwargs["p_id"]
        ).order_by("-created")


class ListOldAnswersOfPost(ListAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.request.method == "GET":
            return AnswerSerializer_detailed
        if self.request.method == "POST":
            return AnswerSerializer

    def get_queryset(self):
        return Answer.objects.filter(
            post__id=self.kwargs["p_id"]
        ).order_by("created")


class ListPopularAnswersOfPost(ListAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.request.method == "GET":
            return AnswerSerializer_detailed
        if self.request.method == "POST":
            return AnswerSerializer

    def get_queryset(self):
        return Answer.objects.filter(
            post__id=self.kwargs["p_id"]
        ).order_by("votes")


class DetailAnswersOfPost(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Answer.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return AnswerSerializer_detailed
        return AnswerSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        conditions = {
            "post__id": self.kwargs["p_id"],
            "id": self.kwargs["a_id"],
        }
        return get_object_or_404(queryset, **conditions)

    def put(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)


class ListAnswersOfUser(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.request.method == "GET":
            return AnswerSerializer_detailed
        if self.request.method == "POST":
            return AnswerSerializer

    def get_queryset(self):
        return Answer.objects.filter(
            author__username=self.kwargs["username"]
        ).order_by("-created")


class DetailAnswersOfUser(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Answer.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return AnswerSerializer_detailed
        return AnswerSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        conditions = {
            "author__username": self.kwargs["username"],
            "id": self.kwargs["a_id"],
        }
        return get_object_or_404(queryset, **conditions)

    def put(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)
