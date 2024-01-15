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
from post.api.serializers import *
from directory.models import *
from post.models import *
from account.models import User
from extensions.pagination import CustomPagination
from notifications.models import Notification

from rest_framework import viewsets, exceptions
from rest_framework.response import Response
from rest_framework.generics import *
from rest_framework.permissions import *
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import (
    RetrieveUpdateAPIView,
    CreateAPIView,
    ListAPIView,
    UpdateAPIView,
    RetrieveAPIView,
    DestroyAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticated

# TODO Notifications automatically from the page you are part of


class CreateDirectoryView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = DirectorySerializer
    parser_classes = (FormParser, MultiPartParser)

    def create(self, request, *args, **kwargs):
        avatar = request.data.get("avatar")
        cover = request.data.get("cover")
        name = request.data.get("name")
        description = request.data.get("description")
        directory_type = request.data.get("directory_type")
        category = request.data.get("category")
        username = request.data.get("username")
        creator = get_object_or_404(User, username=username)

        with transaction.atomic():
            directory = Directory.objects.create(
                creator=creator, 
                name=name, 
                directory_type=directory_type, 
                category=category, 
                avatar=avatar, 
                cover=cover, 
                description=description
            )
        d = DirectorySerializer(directory).data
        return Response({
                "success": "Your directory has been created successfully.",
            }, status=status.HTTP_201_CREATED)


class DirectoryDetailView(RetrieveAPIView):
    lookup_field = "name"
    permission_classes = (IsAuthenticated,)
    serializer_class = DirectoryDetailSerializer
    queryset = Directory.objects.all()


class DirectoryUpdateView(UpdateAPIView):
    lookup_field = "name"
    permission_classes = (IsAuthenticated,)
    serializer_class = DirectorySerializer
    queryset = Directory.objects.all()
    parser_classes = (FormParser, MultiPartParser)


class DirectoryDeleteView(DestroyAPIView):
    lookup_field = "name"
    permission_classes = (IsAuthenticated,)
    serializer_class = DirectorySerializer
    queryset = Directory.objects.all()


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def user_creator_directory(request):
    if request.method == "POST":
        pk = request.data.get("pk")
        directory = get_object_or_404(Directory, id=pk)
        if request.user is directory.creator:
            creator = True
        else:
            creator = False
        return Response(
            {
                "success": creator,
            },
            status=status.HTTP_200_OK,
        )
    return Response({
                    "error": "There was an unforeseen error.",
                }, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def user_joined_directory(request):
    if request.method == "POST":
        pk = request.data.get("pk")
        directory = get_object_or_404(Directory, id=pk)
        if request.user in directory.subscribers.all():
            joined = True
        else:
            joined = False
        return Response(
            {
                "success": joined,
            },
            status=status.HTTP_200_OK,
        )
    return Response({
                    "Error": "There was an unforeseen error.",
                }, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def join_directory(request):
    if request.method == "POST":
        pk = request.data.get("pk")
        directory = get_object_or_404(Directory, id=pk)
        if request.user in directory.subscribers.all():
            joined = False
            directory.subscribers.remove(request.user)
            directory.subscriber_count = directory.subscriber_count - 1
            directory.save()
        else:
            joined = True
            directory.subscribers.add(request.user)
            directory.subscriber_count = directory.subscriber_count + 1
            directory.save()
        return Response(
            {
                "success": joined,
            },
            status=status.HTTP_201_CREATED,
        )
    return Response({
                    "error": "There was an unforeseen error.",
                }, status=status.HTTP_400_BAD_REQUEST)


class ListLinksOfDirectory(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LinkSerializer
    queryset = Link.objects.all()

    def get(self, request, name):
        link = Link.objects.filter(organization__name=name)
        serializer = LinkSerializer(link, many=True)
        return Response(
            {
                "success": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class CreateLinkView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)
    serializer_class = LinkSerializer
    parser_classes = (FormParser, MultiPartParser)

    def create(self, request, *args, **kwargs):
        name = request.data.get("name")
        title = request.data.get("title")
        image = request.data.get("image")
        url = request.data.get("url")
        directory = Directory.objects.get(name=name)

        with transaction.atomic():
            link = Link.objects.create(directory=directory, image=image, title=title, url=url)
        d = LinkSerializer(link).data
        return Response({
                "success": d.data,
            },
            status=status.HTTP_201_CREATED
        )


class LinkDeleteView(DestroyAPIView):
    lookup_field = "id"
    permission_classes = (IsAuthenticated,)
    serializer_class = LinkSerializer
    queryset = Link.objects.all()


class ListRulesOfDirectory(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RuleSerializer
    queryset = Rule.objects.all()

    def list(self, request, name):
        rule = Rule.objects.filter(directory__name=name)
        serializer = RuleSerializer(rule, many=True)
        return Response({
                "success": serializer.data,
            }, 
            status=status.HTTP_200_OK
        )


class CreateRuleView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)
    serializer_class = RuleSerializer
    parser_classes = (FormParser, MultiPartParser)

    def create(self, request, *args, **kwargs):
        name = request.data.get("name")
        title = request.data.get("title")
        text = request.data.get("text")
        directory = Directory.objects.get(name=name)

        with transaction.atomic():
            rule = Rule.objects.create(directory=directory, text=text, title=title)
        d = RuleSerializer(rule).data
        return Response({
                "success": d.data,
            }, 
            status=status.HTTP_201_CREATED
        )


class RuleDeleteView(DestroyAPIView):
    lookup_field = "id"
    permission_classes = (IsAuthenticated,)
    serializer_class = RuleSerializer
    queryset = Rule.objects.all()


class ListDirectoriesOfUser(ListAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    serializer_class = DirectorySerializer

    def get(self, request, username):
        directory = Directory.objects.filter(creator__username=username)
        serializer = self.serializer_class(directory, many=True)
        return Response({
                "success": serializer.data,
            }, 
            status=status.HTTP_200_OK
        )


class ListDirectoriesUserIsModerator(ListAPIView):
    queryset=Directory.objects.all()
    serializer_class=DirectorySerializer
    permission_classes=(IsAuthenticated,)

    def get_queryset(self):
        directories = Directory.objects.filter(moderators=self.request.user)
        return Response({
                "success": directories,
            }, 
            status=status.HTTP_200_OK
        )


class ListDirectoriesUserIsJoined(ListAPIView):
    queryset=Directory.objects.all()
    serializer_class=DirectorySerializer
    permission_classes=(IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        directories = Directory.objects.filter(subscribers=user)
        return Response({
                "success": directories,
            }, 
            status=status.HTTP_200_OK
        )

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def ListPostsOfDirectory(request, directory_name):
    post = Post.objects.filter(
            directory__name=directory_name, is_reviewed=True, is_deleted=False
        )
    paginator = CustomPagination()
    result_directory = paginator.paginate_queryset(post,request)

    serializer = PostSerializer_detailed(result_directory, many=True, context={
                                        'request': request
                                        })
    return paginator.get_paginated_response({'data':serializer.data},status=status.HTTP_200_OK)     
    

class DetailPostOfDirectory(RetrieveUpdateDestroyAPIView):
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

