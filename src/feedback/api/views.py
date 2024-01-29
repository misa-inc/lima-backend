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
from feedback.models import *
from account.models import User
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
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    UpdateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListCreateAPIView
)

# TODO Add Lima Aura as the gift users get from posting, commenting and voting

class CreateFeedbackView(CreateAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer,)
    serializer_class = FeedbackSerializer

    def create(self, request, *args, **kwargs):
        title = request.data.get("title")
        pk = request.data.get("pk")
        attachment = request.data.get("attachment")
        video = request.data.get("video")
        board = request.data.get("board")
        status = request.data.get("status")
        file = request.data.get("file")
        link = request.data.get("link")
        text = request.data.get("text")
        post_type = request.data.get("post_type")
        author = request.user

        with transaction.atomic():
            post = Feedback.objects.create(
                title=title,
                attachment=attachment,
                video=video,
                link=link,
                status=status,
                file=file,
                board=board,
                text=text,
                author=author,
                post_type=post_type,
            )
        d = FeedbackSerializer(post).data
        return Response(d, status=status.HTTP_201_CREATED)


class FeedbackCreateView(CreateAPIView):
    permission_classes = (AllowAny,)
    parser_classes = (FormParser, MultiPartParser)
    serializer_class = FeedbackSerializer

    def create(self, request, *args, **kwargs):
        title = request.data.get("title")
        pk = request.data.get("pk")
        attachment = request.data.get("attachment")
        video = request.data.get("video")
        board = request.data.get("board")
        status = request.data.get("status")
        file = request.data.get("file")
        link = request.data.get("link")
        text = request.data.get("text")
        post_type = request.data.get("post_type")
        author = request.user

        with transaction.atomic():
            post = Feedback.objects.create(
                title=title,
                attachment=attachment,
                video=video,
                link=link,
                status=status,
                file=file,
                board=board,
                text=text,
                author=author,
                post_type=post_type,
            )
        d = FeedbackSerializer(post).data
        return Response(d, status=status.HTTP_201_CREATED)


class FeedbackUpdateView(UpdateAPIView):
    lookup_field = "id"
    permission_classes = (AllowAny,)
    parser_classes = (FormParser, MultiPartParser)
    serializer_class = FeedbackSerializer
    queryset = Feedback.objects.all()


class FeedbackDeleteView(APIView):
    permission_classes = (AllowAny, )

    def post(self,request):
        data = request.data
        post = get_object_or_404(Feedback,id=data.get('post_id'))
        if post.author == request.user:
            post.delete()
            return Response({"post_deleted": True})


@api_view(['GET'])
@permission_classes((AllowAny,))
def ListFeedbacksOfUser(request, username):
    post = Feedback.objects.filter(
            author__username=username, is_reviewed=True, is_deleted=False
        )
    paginator = CustomPagination()
    result_page = paginator.paginate_queryset(post,request)

    serializer = FeedbackSerializer_detailed(result_page, many=True, context={
                                        
                                        'request': request
                                        })
    return paginator.get_paginated_response({'data':serializer.data})    
    

class DetailFeedbackOfUser(RetrieveUpdateDestroyAPIView):
    permission_classes = (AllowAny,)
    queryset = Feedback.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return FeedbackSerializer_detailed
        return FeedbackSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        conditions = {
            "author__username": self.kwargs["username"],
            "id": self.kwargs["p_id"],
        }
        return get_object_or_404(queryset, **conditions)

    def put(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)


@api_view(["POST"])
@permission_classes((AllowAny,))
def user_reported_feedback(request):
    if request.method == "POST":
        pk = request.data.get("pk")
        post = get_object_or_404(Feedback, id=pk)
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
@permission_classes((AllowAny,))
def report_feedback(request):
    if request.method == "POST":
        pk = request.data.get("pk")
        post = get_object_or_404(Feedback, id=pk)
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
@permission_classes((AllowAny,))
def VoteOnFeedback(request):
    if request.method == "POST":
        voter = request.user
        post_id = request.data.get("post_id")
        value = request.data.get("value")
        post = get_object_or_404(Feedback, id=post_id)

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
            {"post": FeedbackSerializer(get_object_or_404(Feedback, id=post_id)).data},
                status=status.HTTP_201_CREATED,
        )        
        
        

class RetrieveFeedback(ListAPIView):
    queryset = Feedback.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = FeedbackSerializer

    def get(self, request, pk):
        post = Feedback.objects.get(id=pk)
        serializer = self.serializer_class(post)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes((AllowAny,))
def user_voted_feedback(request):
    if request.method == "POST":
        voter = request.user
        pk = request.data.get("pk")
        post = get_object_or_404(Feedback, id=pk)
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
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer,)
    serializer_class = CommentSerializer

    def create(self, request, *args, **kwargs):
        author = request.user
        post_id = request.data.get("post_id")
        text = request.data.get("text")
        parent_comment_id = request.data.get("parent_comment_id")
        post = get_object_or_404(Feedback, id=post_id)

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

        d = CommentSerializer(comment).data
        return Response(d, status=status.HTTP_201_CREATED)


class CommentUpdateView(UpdateAPIView):
    lookup_field = "id"
    permission_classes = (AllowAny,)
    parser_classes = (FormParser, MultiPartParser)
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()


class CommentDeleteView(APIView):
    permission_classes = (AllowAny, )

    def post(self,request):
        data = request.data
        comment = get_object_or_404(Comment,id=data.get('comment_id'))
        if comment.author == request.user:
            comment.delete()
            return Response({"post_deleted": True})

    
@api_view(["POST"])
@permission_classes((AllowAny,))
def VoteOnComment(request):
    if request.method == "POST":
        voter = request.user
        comment_id = request.data.get("comment_id")
        value = request.data.get("value")
        comment = get_object_or_404(Comment, id=comment_id)

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
                "comment": CommentSerializer(
                    get_object_or_404(Comment, id=comment_id)
                ).data
            },
            status=status.HTTP_201_CREATED,
        )


@api_view(["POST"])
@permission_classes((AllowAny,))
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
@permission_classes((AllowAny,))
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
@permission_classes((AllowAny,))
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


class ListNewCommentsOfFeedback(ListAPIView):
    permission_classes = (AllowAny,)
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


class ListOldCommentsOfFeedback(ListAPIView):
    permission_classes = (AllowAny,)
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


class ListPopularCommentsOfFeedback(ListAPIView):
    permission_classes = (AllowAny,)
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


class DetailCommentsOfFeedback(RetrieveUpdateDestroyAPIView):
    permission_classes = (AllowAny,)
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
    permission_classes = (AllowAny,)
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
    permission_classes = (AllowAny,)
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
