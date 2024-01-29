import jwt
import os
import random
import string
import re
from datetime import datetime, timedelta
 
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
from discussion.models import *
from account.models import User
from extensions.pagination import CustomPagination
from notifications.models import Notification

from rest_framework import viewsets, exceptions
from rest_framework.permissions import IsAuthenticated, IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import *
from rest_framework.permissions import *
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    UpdateAPIView,
    RetrieveAPIView,
    DestroyAPIView,
)

 
class CreateDiscussionView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = DiscussionSerializer
    parser_classes = (FormParser, MultiPartParser)

    def create(self, request, *args, **kwargs):
        avatar = request.data.get("avatar")
        cover = request.data.get("cover")
        discussion_name = request.data.get("discussion_name")
        discussion_type = request.data.get("discussion_type")
        category = request.data.get("category")
        category_id = request.data.get("category_id")
        directory_id = request.data.get("directory_id")
        is_request = request.data.get("is_request")
        username = request.data.get("username")
        directory = get_object_or_404(Directory, id=directory_id)
        category = get_object_or_404(Category, id=category_id)
        creator = get_object_or_404(User, username=username)

        with transaction.atomic():
            if is_request == "1":
                discussion = Discussion.objects.create(
                    creator=creator, 
                    discussion_name=discussion_name, 
                    discussion_type=discussion_type, 
                    category=category, 
                    directory=directory,
                    avatar=avatar, 
                    cover=cover,
                    is_request=True 
                )
            else:
                discussion = Discussion.objects.create(
                    creator=creator, 
                    discussion_name=discussion_name, 
                    discussion_type=discussion_type, 
                    category=category, 
                    directory=directory,
                    avatar=avatar, 
                    cover=cover
                )
        d = DiscussionSerializer(discussion).data
        return Response(d, status=status.HTTP_201_CREATED)


class DiscussionDetailView(RetrieveAPIView):
    lookup_field = "id"
    permission_classes = (IsAuthenticated,)
    serializer_class = DiscussionSerializer
    queryset = Discussion.objects.all()


class DiscussionUpdateView(UpdateAPIView):
    lookup_field = "id"
    permission_classes = (IsAuthenticated,)
    serializer_class = DiscussionSerializer
    queryset = Discussion.objects.all()
    parser_classes = (FormParser, MultiPartParser)


class DiscussionDeleteView(DestroyAPIView):
    lookup_field = "id"
    permission_classes = (IsAuthenticated,)
    serializer_class = DiscussionSerializer
    queryset = Discussion.objects.all()


class ListDiscussionsOfUsers(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = DiscussionSerializer
    queryset = Discussion.objects.all()

    def get(self, request):
        discussion = Discussion.objects.filter(creator=self.request.user)
        serializer = DiscussionSerializer(discussion, many=True)
        return Response(serializer.data)


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def user_creator_discussion(request):
    if request.method == "POST":
        pk = request.data.get("pk")
        discussion = get_object_or_404(Discussion, id=pk)
        if request.user is discussion.creator:
            creator = True
        else:
            creator = False
        return Response(
            {
                "creator": creator,
            },
            status=status.HTTP_200_OK,
        )


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def user_joined_discussion(request):
    if request.method == "POST":
        pk = request.data.get("pk")
        discussion = get_object_or_404(Discussion, id=pk)
        if request.user in discussion.subscribed_users.all():
            joined = True
        else:
            joined = False
        return Response(
            {
                "joined": joined,
            },
            status=status.HTTP_200_OK,
        )


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def join_discussion(request):
    if request.method == "POST":
        pk = request.data.get("pk")
        discussion = get_object_or_404(Discussion, id=pk)
        if request.user in discussion.subscribed_users.all():
            joined = False
            discussion.subscribed_users.remove(request.user)
            discussion.subscriber_count = discussion.subscriber_count - 1
            discussion.save()
        else:
            joined = True
            discussion.subscribed_users.add(request.user)
            discussion.subscriber_count = discussion.subscriber_count + 1
            discussion.save()
        return Response(
            {
                "joined": joined,
            },
            status=status.HTTP_201_CREATED,
        )


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def user_blocked_in_discussion(request):
    if request.method == "POST":
        pk = request.data.get("pk")
        discussion = get_object_or_404(Discussion, id=pk)
        if request.user in discussion.blocked_users.all():
            blocked = True
        else:
            blocked = False
        return Response(
            {
                "blocked": blocked,
            },
            status=status.HTTP_200_OK,
        )


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def block_user_in_discussion(request):
    if request.method == "POST":
        pk = request.data.get("pk")
        discussion = get_object_or_404(Discussion, id=pk)
        if request.user in discussion.blocked_users.all():
            blocked = False
            discussion.blocked_users.remove(request.user)
            discussion.save()
        else:
            blocked = True
            discussion.blocked_users.add(request.user)
            discussion.save()
        return Response(
            {
                "blocked": blocked,
            },
            status=status.HTTP_201_CREATED,
        )


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def user_liked_discussion(request):
    if request.method == "POST":
        pk = request.data.get("pk")
        discussion = get_object_or_404(Discussion, id=pk)
        if request.user in discussion.liked_users.all():
            liked = True
        else:
            liked = False
        return Response(
            {
                "liked": liked,
            },
            status=status.HTTP_200_OK,
        )


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def like_discussion(request):
    if request.method == "POST":
        pk = request.data.get("pk")
        discussion = get_object_or_404(Discussion, id=pk)
        if request.user in discussion.liked_users.all():
            liked = False
            discussion.liked_users.remove(request.user)
            discussion.like_count = discussion.like_count - 1
            discussion.save()
        else:
            liked = True
            discussion.liked_users.add(request.user)
            discussion.like_count = discussion.like_count + 1
            discussion.save()
        return Response(
            {
                "liked": liked,
            },
            status=status.HTTP_201_CREATED,
        )


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def added_moderator(request):
    if request.method == "POST":
        pk = request.data.get("pk")
        discussion = get_object_or_404(Discussion, id=pk)
        if request.user in discussion.moderator_users.all():
            added = True
        else:
            added = False
        return Response(
            {
                "added": added,
            },
            status=status.HTTP_200_OK,
        )


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def add_remove_moderator(request):
    if request.method == "POST":
        pk = request.data.get("pk")
        moderator_id = request.data.get("moderator_id")
        moderator = get_object_or_404(User, id=moderator_id)
        discussion = get_object_or_404(Discussion, id=pk)
        if moderator in discussion.moderator_users.all():
            added = False
            discussion.moderator_users.remove(moderator)
            #discussion.subscriber_count = discussion.subscriber_count - 1
            discussion.save()
        else:
            added = True
            discussion.moderator_users.add(moderator)
            #discussion.subscriber_count = discussion.subscriber_count + 1
            discussion.save()
        return Response(
            {
                "added": added,
            },
            status=status.HTTP_201_CREATED,
        )


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def add_remove_project(request):
    if request.method == "POST":
        pk = request.data.get("pk")
        project_id = request.data.get("project_id")
        project = get_object_or_404(Project, id=project_id)
        discussion = get_object_or_404(Discussion, id=pk)
        if project in discussion.projects.all():
            added = False
            discussion.projects.remove(project)
            #discussion.subscriber_count = discussion.subscriber_count - 1
            discussion.save()
        else:
            added = True
            discussion.projects.add(project)
            #discussion.subscriber_count = discussion.subscriber_count + 1
            discussion.save()
        return Response(
            {
                "added": added,
            },
            status=status.HTTP_201_CREATED,
        )


class CreateBotView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BotSerializer
    parser_classes = (FormParser, MultiPartParser)

    def create(self, request, *args, **kwargs):
        file_name = request.data.get("file_name")
        file = request.data.get("file")
        message_handler = request.data.get("message_handler")
        description = request.data.get("description")
        username = request.data.get("username")
        user = get_object_or_404(User, username=username)

        with transaction.atomic():
            bot = Bot.objects.create(
                user=user, 
                file_name=file_name,
                file=file,  
                message_handler=message_handler, 
                description=description
            )
        d = BotSerializer(bot).data
        return Response(d, status=status.HTTP_201_CREATED)


class BotDetailView(RetrieveAPIView):
    lookup_field = "id"
    permission_classes = (IsAuthenticated,)
    serializer_class = BotSerializer
    queryset = Bot.objects.all()


class BotUpdateView(UpdateAPIView):
    lookup_field = "id"
    permission_classes = (IsAuthenticated,)
    serializer_class = BotSerializer
    queryset = Bot.objects.all()


class BotDeleteView(DestroyAPIView):
    lookup_field = "id"
    permission_classes = (IsAuthenticated,)
    serializer_class = BotSerializer
    queryset = Bot.objects.all()


class CreateCategoryView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CategorySerializer

    def create(self, request, *args, **kwargs):
        avatar = request.data.get("avatar")
        title = request.data.get("title")
        description = request.data.get("description")
        needs_answer = request.data.get("needs_answer")
        directory_id = request.data.get("directory_id")
        directory = get_object_or_404(Directory, directory_id=directory_id)

        with transaction.atomic():
            if needs_answer == "1":
                category = Category.objects.create(
                    directory=directory, 
                    avatar=avatar, 
                    title=title, 
                    description=description,
                    needs_answer=True
                )
            else:
                category = Category.objects.create(
                    directory=directory, 
                    avatar=avatar, 
                    title=title, 
                    description=description
                )    
        d = CategorySerializer(category).data
        return Response(d, status=status.HTTP_201_CREATED)


class CategoryDetailView(RetrieveAPIView):
    lookup_field = "id"
    permission_classes = (IsAuthenticated,)
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class CategoryUpdateView(UpdateAPIView):
    lookup_field = "id"
    permission_classes = (IsAuthenticated,)
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class CategoryDeleteView(DestroyAPIView):
    lookup_field = "id"
    permission_classes = (IsAuthenticated,)
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


@api_view(['GET'])
def getMe(request):
    ip_addr = request.META.get('HTTP_X_FORWADED_FOR') or request.META.get('REMOTE_ADDR')
    user_agent = request.META.get('HTTP_USER_AGENT')

    return Response(
        {
            'ip_address':ip_addr,
            'user_agent':user_agent
        }
    )


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def ListChatsOfDiscussion(request, id):
    discussion_chats = Chat.objects.filter(discussion__id=id)
    paginator = CustomPagination()
    result_page = paginator.paginate_queryset(discussion_chats,request)

    serializer = ChatSerializer(result_page, many=True, context={'request': request})
    return paginator.get_paginated_response({'data':serializer.data})    


class ChatDeleteView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        data = request.data
        chat = get_object_or_404(Chat,id=data.get('chat_id'))
        if chat.from_user == request.user:
            chat.delete()
            return Response({"chat_deleted": True})
        return Response({"chat_deleted": False})

