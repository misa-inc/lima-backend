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
from collection.models import *
from post.models import *
from trivia.models import *
from events.models import *
from blog.models import *
from library.models import *
from directory.models import *
from discussion.models import *
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


class CreateCollectionView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CollectionSerializer
    parser_classes = (FormParser, MultiPartParser)

    def create(self, request, *args, **kwargs):
        name = request.data.get("name")
        description = request.data.get("description")
        collection_type = request.data.get("collection_type")
        username = request.data.get("username")
        creator = get_object_or_404(User, username=username)

        with transaction.atomic():
            collection = Collection.objects.create(
                creator=creator, 
                name=name, 
                collection_type=collection_type, 
                description=description
            )
        d = CollectionSerializer(collection).data
        return Response({
                "success": "Your Collection has been created successfully.",
            }, status=status.HTTP_201_CREATED)


class CollectionDetailView(RetrieveAPIView):
    lookup_field = "name"
    permission_classes = (IsAuthenticated,)
    serializer_class = CollectionDetailSerializer
    queryset = Collection.objects.all()


class CollectionUpdateView(UpdateAPIView):
    lookup_field = "name"
    permission_classes = (IsAuthenticated,)
    serializer_class = CollectionSerializer
    queryset = Collection.objects.all()
    parser_classes = (FormParser, MultiPartParser)


class CollectionDeleteView(DestroyAPIView):
    lookup_field = "name"
    permission_classes = (IsAuthenticated,)
    serializer_class = CollectionSerializer
    queryset = Collection.objects.all()


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def user_creator_collection(request):
    if request.method == "POST":
        pk = request.data.get("pk")
        collection = get_object_or_404(Collection, id=pk)
        if request.user is collection.creator:
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
def user_collected_post(request):
    if request.method == "POST":
        collection_pk = request.data.get("collection_pk")
        post_pk = request.data.get("post_pk")
        collection = get_object_or_404(Collection, id=collection_pk)
        post = get_object_or_404(Post, id=post_pk)
        if post in collection.posts.all():
            collected = False
        else:
            collected = True
        return Response(
            {
                "success": collected,
            },
            status=status.HTTP_200_OK,
        )
    return Response({
                    "Error": "There was an unforeseen error.",
                }, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def collect_post(request):
    if request.method == "POST":
        collection_pk = request.data.get("collection_pk")
        post_pk = request.data.get("post_pk")
        collection = get_object_or_404(Collection, id=collection_pk)
        post = get_object_or_404(Post, id=post_pk)
        if post in collection.posts.all():
            collected = False
            collection.posts.remove(post)
            collection.save()
        else:
            collected = True
            collection.posts.add(post)
            collection.save()
        return Response(
            {
                "success": collected,
            },
            status=status.HTTP_201_CREATED,
        )
    return Response({
                    "error": "There was an unforeseen error.",
                }, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def user_collected_trivia(request):
    if request.method == "POST":
        collection_pk = request.data.get("collection_pk")
        trivia_pk = request.data.get("trivia_pk")
        collection = get_object_or_404(Collection, id=collection_pk)
        trivia = get_object_or_404(Trivia, id=trivia_pk)
        if trivia in collection.trivias.all():
            collected = False
        else:
            collected = True
        return Response(
            {
                "success": collected,
            },
            status=status.HTTP_200_OK,
        )
    return Response({
                    "Error": "There was an unforeseen error.",
                }, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def collect_trivia(request):
    if request.method == "POST":
        collection_pk = request.data.get("collection_pk")
        trivia_pk = request.data.get("trivia_pk")
        collection = get_object_or_404(Collection, id=collection_pk)
        trivia = get_object_or_404(Trivia, id=trivia_pk)
        if trivia in collection.trivias.all():
            collected = False
            collection.trivias.remove(trivia)
            collection.save()
        else:
            collected = True
            collection.trivias.add(trivia)
            collection.save()
        return Response(
            {
                "success": collected,
            },
            status=status.HTTP_201_CREATED,
        )
    return Response({
                    "error": "There was an unforeseen error.",
                }, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def user_collected_event(request):
    if request.method == "POST":
        collection_pk = request.data.get("collection_pk")
        event_pk = request.data.get("event_pk")
        collection = get_object_or_404(Collection, id=collection_pk)
        event = get_object_or_404(Event, id=event_pk)
        if event in collection.events.all():
            collected = False
        else:
            collected = True
        return Response(
            {
                "success": collected,
            },
            status=status.HTTP_200_OK,
        )
    return Response({
                    "Error": "There was an unforeseen error.",
                }, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def collect_event(request):
    if request.method == "POST":
        collection_pk = request.data.get("collection_pk")
        event_pk = request.data.get("event_pk")
        collection = get_object_or_404(Collection, id=collection_pk)
        event = get_object_or_404(Event, id=event_pk)
        if event in collection.events.all():
            collected = False
            collection.events.remove(event)
            collection.save()
        else:
            collected = True
            collection.events.add(event)
            collection.save()
        return Response(
            {
                "success": collected,
            },
            status=status.HTTP_201_CREATED,
        )
    return Response({
                    "error": "There was an unforeseen error.",
                }, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def user_collected_article(request):
    if request.method == "POST":
        collection_pk = request.data.get("collection_pk")
        article_pk = request.data.get("article_pk")
        collection = get_object_or_404(Collection, id=collection_pk)
        article = get_object_or_404(Blog, id=article_pk)
        if article in collection.articles.all():
            collected = False
        else:
            collected = True
        return Response(
            {
                "success": collected,
            },
            status=status.HTTP_200_OK,
        )
    return Response({
                    "Error": "There was an unforeseen error.",
                }, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def collect_article(request):
    if request.method == "POST":
        collection_pk = request.data.get("collection_pk")
        article_pk = request.data.get("article_pk")
        collection = get_object_or_404(Collection, id=collection_pk)
        article = get_object_or_404(Blog, id=article_pk)
        if article in collection.articles.all():
            collected = False
            collection.articles.remove(article)
            collection.save()
        else:
            collected = True
            collection.articles.add(article)
            collection.save()
        return Response(
            {
                "success": collected,
            },
            status=status.HTTP_201_CREATED,
        )
    return Response({
                    "error": "There was an unforeseen error.",
                }, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def user_collected_book(request):
    if request.method == "POST":
        collection_pk = request.data.get("collection_pk")
        book_pk = request.data.get("book_pk")
        collection = get_object_or_404(Collection, id=collection_pk)
        book = get_object_or_404(Book, id=book_pk)
        if book in collection.books.all():
            collected = False
        else:
            collected = True
        return Response(
            {
                "success": collected,
            },
            status=status.HTTP_200_OK,
        )
    return Response({
                    "Error": "There was an unforeseen error.",
                }, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def collect_book(request):
    if request.method == "POST":
        collection_pk = request.data.get("collection_pk")
        book_pk = request.data.get("book_pk")
        collection = get_object_or_404(Collection, id=collection_pk)
        book = get_object_or_404(Book, id=book_pk)
        if book in collection.books.all():
            collected = False
            collection.books.remove(book)
            collection.save()
        else:
            collected = True
            collection.books.add(book)
            collection.save()
        return Response(
            {
                "success": collected,
            },
            status=status.HTTP_201_CREATED,
        )
    return Response({
                    "error": "There was an unforeseen error.",
                }, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def user_collected_directory(request):
    if request.method == "POST":
        collection_pk = request.data.get("collection_pk")
        directory_pk = request.data.get("directory_pk")
        collection = get_object_or_404(Collection, id=collection_pk)
        directory = get_object_or_404(Directory, id=directory_pk)
        if directory in collection.directories.all():
            collected = False
        else:
            collected = True
        return Response(
            {
                "success": collected,
            },
            status=status.HTTP_200_OK,
        )
    return Response({
                    "Error": "There was an unforeseen error.",
                }, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def collect_directory(request):
    if request.method == "POST":
        collection_pk = request.data.get("collection_pk")
        directory_pk = request.data.get("directory_pk")
        collection = get_object_or_404(Collection, id=collection_pk)
        directory = get_object_or_404(Directory, id=directory_pk)
        if directory in collection.directories.all():
            collected = False
            collection.directories.remove(directory)
            collection.save()
        else:
            collected = True
            collection.directories.add(directory)
            collection.save()
        return Response(
            {
                "success": collected,
            },
            status=status.HTTP_201_CREATED,
        )
    return Response({
                    "error": "There was an unforeseen error.",
                }, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def user_collected_discussion(request):
    if request.method == "POST":
        collection_pk = request.data.get("collection_pk")
        discussion_pk = request.data.get("discussion_pk")
        collection = get_object_or_404(Collection, id=collection_pk)
        discussion = get_object_or_404(Discussion, id=discussion_pk)
        if discussion in collection.discussions.all():
            collected = False
        else:
            collected = True
        return Response(
            {
                "success": collected,
            },
            status=status.HTTP_200_OK,
        )
    return Response({
                    "Error": "There was an unforeseen error.",
                }, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def collect_discussion(request):
    if request.method == "POST":
        collection_pk = request.data.get("collection_pk")
        discussion_pk = request.data.get("discussion_pk")
        collection = get_object_or_404(Collection, id=collection_pk)
        discussion = get_object_or_404(Discussion, id=discussion_pk)
        if discussion in collection.discussions.all():
            collected = False
            collection.discussions.remove(discussion)
            collection.save()
        else:
            collected = True
            collection.discussions.add(discussion)
            collection.save()
        return Response(
            {
                "success": collected,
            },
            status=status.HTTP_201_CREATED,
        )
    return Response({
                    "error": "There was an unforeseen error.",
                }, status=status.HTTP_400_BAD_REQUEST)


class ListCollectionsOfUser(ListAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    serializer_class = CollectionSerializer

    def get(self, request):
        username = request.data.get("username")
        collection = Collection.objects.filter(creator__username=username, is_deleted=False)
        serializer = self.serializer_class(collection, many=True)
        return Response({
                "success": serializer.data,
            }, 
            status=status.HTTP_200_OK
        )


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def DetailCollectionOfUser(request):
    collection_pk = request.data.get("collection_pk")
    collection = Collection.objects.filter(
            id=collection_pk, is_deleted=False
        )
    paginator = CustomPagination()
    result_collection = paginator.paginate_queryset(collection,request)

    serializer = CollectionDetailSerializer(result_collection, many=True, context={'request': request})
    return paginator.get_paginated_response({'data':serializer.data},status=status.HTTP_200_OK)     
 