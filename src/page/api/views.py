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
from page.models import *
from post.models import *
from post.api.serializers import *
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
    RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import AllowAny, IsAuthenticated

# TODO Notifications automatically from the page you are part of


class CreatePageView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PageSerializer
    parser_classes = (FormParser, MultiPartParser)

    def create(self, request, *args, **kwargs):
        avatar = request.data.get("avatar")
        cover = request.data.get("cover")
        name = request.data.get("name")
        description = request.data.get("description")
        page_type = request.data.get("page_type")
        category = request.data.get("category")
        username = request.data.get("username")
        creator = get_object_or_404(User, username=username)

        with transaction.atomic():
            Page = Page.objects.create(
                creator=creator, 
                name=name, 
                page_type=page_type, 
                category=category, 
                avatar=avatar, 
                cover=cover, 
                description=description
            )
        d = PageSerializer(Page).data
        return Response({
                "success": "Your page has been created successfully.",
            }, status=status.HTTP_201_CREATED)


class PageDetailView(RetrieveAPIView):
    lookup_field = "name"
    permission_classes = (IsAuthenticated,)
    serializer_class = PageDetailSerializer
    queryset = Page.objects.all()


class PageUpdateView(UpdateAPIView):
    lookup_field = "name"
    permission_classes = (IsAuthenticated,)
    serializer_class = PageSerializer
    queryset = Page.objects.all()
    parser_classes = (FormParser, MultiPartParser)


class PageDeleteView(DestroyAPIView):
    lookup_field = "name"
    permission_classes = (IsAuthenticated,)
    serializer_class = PageSerializer
    queryset = Page.objects.all()


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def user_creator_page(request):
    if request.method == "POST":
        pk = request.data.get("pk")
        page = get_object_or_404(Page, id=pk)
        if request.user is page.creator:
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
def user_joined_page(request):
    if request.method == "POST":
        pk = request.data.get("pk")
        page = get_object_or_404(Page, id=pk)
        if request.user in page.subscribers.all():
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
def join_page(request):
    if request.method == "POST":
        pk = request.data.get("pk")
        page = get_object_or_404(Page, id=pk)
        if request.user in page.subscribers.all():
            joined = False
            page.subscribers.remove(request.user)
            page.subscriber_count = page.subscriber_count - 1
            page.save()
        else:
            joined = True
            page.subscribers.add(request.user)
            page.subscriber_count = page.subscriber_count + 1
            page.save()
        return Response(
            {
                "success": joined,
            },
            status=status.HTTP_201_CREATED,
        )
    return Response({
                    "error": "There was an unforeseen error.",
                }, status=status.HTTP_400_BAD_REQUEST)


class ListLinksOfPage(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LinkSerializer
    queryset = Link.objects.all()

    def get(self, request, name):
        link = Link.objects.filter(page__name=name)
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
        page = Page.objects.get(name=name)

        with transaction.atomic():
            link = Link.objects.create(page=page, image=image, title=title, url=url)
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


class ListRulesOfPage(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RuleSerializer
    queryset = Rule.objects.all()

    def list(self, request, name):
        rule = Rule.objects.filter(page__name=name)
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
        page = Page.objects.get(name=name)

        with transaction.atomic():
            rule = Rule.objects.create(page=page, text=text, title=title)
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


class ListPagesOfUser(ListAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    serializer_class = PageSerializer

    def get(self, request, username):
        page = Page.objects.filter(creator__username=username)
        serializer = self.serializer_class(page, many=True)
        return Response({
                "success": serializer.data,
            }, 
            status=status.HTTP_200_OK
        )


class ListPagesUserIsModerator(ListAPIView):
    queryset=Page.objects.all()
    serializer_class=PageSerializer
    permission_classes=(IsAuthenticated,)

    def get_queryset(self):
        pages = Page.objects.filter(moderators=self.request.user)
        return Response({
                "success": pages,
            }, 
            status=status.HTTP_200_OK
        )


class ListPagesUserIsJoined(ListAPIView):
    queryset=Page.objects.all()
    serializer_class=PageSerializer
    permission_classes=(IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        pages = Page.objects.filter(subscribers=user)
        return Response({
                "success": pages,
            }, 
            status=status.HTTP_200_OK
        )

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def ListPostsOfPage(request, page_name):
    post = Post.objects.filter(
            page__name=page_name, is_reviewed=True, is_deleted=False
        )
    paginator = CustomPagination()
    result_page = paginator.paginate_queryset(post,request)

    serializer = PostSerializer_detailed(result_page, many=True, context={
                                        'request': request
                                        })
    return paginator.get_paginated_response({'data':serializer.data},status=status.HTTP_200_OK)     
    

class DetailPostOfPage(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Post.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return PostSerializer_detailed
        return PostSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        conditions = {"page__name": self.kwargs["page_name"], "id": self.kwargs["post_id"]}
        return get_object_or_404(queryset, **conditions)

    def put(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

