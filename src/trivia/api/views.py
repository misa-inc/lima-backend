import jwt
import os
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
from trivia.models import *
from account.models import User
from page.models import *
from directory.models import *
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


class CreateTriviaView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (FormParser, MultiPartParser)
    serializer_class = TriviaSerializer

    def create(self, request, *args, **kwargs):
        attachment = request.data.get("attachment")
        video = request.data.get("video")
        link = request.data.get("link")
        title = request.data.get("title")
        description = request.data.get("description")
        trivia_type = request.data.get("trivia_type")
        page_id = request.data.get("page_id")
        directory_id = request.data.get("directory_id")
        page = get_object_or_404(Page,id=page_id)
        directory = get_object_or_404(Directory,id=directory_id)
        author = request.user

        with transaction.atomic():
                trivia = Trivia.objects.create(
                    attachment = attachment,
                    video = video,
                    link = link,
                    title = title,
                    description = description,
                    trivia_type = trivia_type,
                    author=author,
                    page=page,
                    directory=directory
                )      
        d = TriviaSerializer(trivia).data
        return Response(d, status=status.HTTP_201_CREATED)


class TriviaUpdateView(UpdateAPIView):
    lookup_field = "id"
    permission_classes = (IsAuthenticated,)
    parser_classes = (FormParser, MultiPartParser)
    serializer_class = TriviaSerializer
    queryset = Trivia.objects.all()


class TriviaDeleteView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self,request):
        data = request.data
        trivia = get_object_or_404(Trivia,id=data.get('trivia_id'))
        if trivia.author == request.user:
            trivia.delete()
            return Response({"success": "Trivia has been deleted"})


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def ListTriviaOfUser(request, username):
    trivia = Trivia.objects.filter(
            author__username=username, is_reviewed=True, is_deleted=False
        )
    paginator = CustomPagination()
    result_page = paginator.paginate_queryset(trivia,request)

    serializer = TriviaSerializer_detailed(result_page, many=True, context={'request': request})
    return paginator.get_paginated_response({'data':serializer.data})    
    

class DetailTriviaOfUser(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Trivia.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return TriviaSerializer_detailed
        return TriviaSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        conditions = {
            "author__username": self.kwargs["username"],
            "id": self.kwargs["trivia_id"],
        }
        return get_object_or_404(queryset, **conditions)

    def put(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def user_saved_trivia(request):
    if request.method == "POST":
        pk = request.data.get("pk")
        trivia = get_object_or_404(Trivia, id=pk)
        if request.user in trivia.saved.all():
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
def save_trivia(request):
    if request.method == "POST":
        pk = request.data.get("pk")
        trivia = get_object_or_404(Trivia, id=pk)
        if request.user in trivia.saved.all():
            saved = False
            trivia.saved.remove(request.user)
            trivia.saved_count = trivia.saved_count - 1
            trivia.save()
        else:
            saved = True
            trivia.saved.add(request.user)
            trivia.saved_count = trivia.saved_count + 1
            trivia.save()
        return Response(
            {
                "saved": saved,
            },
            status=status.HTTP_201_CREATED,
        )


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def user_reported_trivia(request):
    if request.method == "POST":
        pk = request.data.get("pk")
        trivia = get_object_or_404(Trivia, id=pk)
        if request.user in trivia.report.all():
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
def report_trivia(request):
    if request.method == "POST":
        pk = request.data.get("pk")
        trivia = get_object_or_404(Trivia, id=pk)
        if request.user in trivia.report.all():
            report = False
            trivia.report.remove(request.user)
            trivia.report_count = trivia.report_count - 1
            trivia.save()
        else:
            report = True
            trivia.report.add(request.user)
            trivia.report_count = trivia.report_count + 1
            trivia.save()
        return Response(
            {
                "report": report,
            },
            status=status.HTTP_201_CREATED,
        )


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def VoteOnTrivia(request):
    if request.method == "POST":
        voter = request.user
        trivia_id = request.data.get("trivia_id")
        value = request.data.get("value")
        trivia = get_object_or_404(Trivia, id=trivia_id)

        if value == 1:
            Notification.objects.get_or_create(
                notification_type="L",
                trivia=trivia,
                comments=(
                    f"@{voter.username} likes your trivia “{trivia.description[:10]}...”"
                ),
                to_user=trivia.author,
                from_user=voter,
            )
        try:
            vote = Vote.objects.get(voter=voter, trivia=trivia)
        except Vote.DoesNotExist:
            vote = Vote.objects.create(voter, value, trivia=trivia)
        else:
            if value == 1:
                vote.value = value
                vote.save()
            elif value == 0:
                vote.delete()

        return Response(
            {"success": TriviaSerializer(get_object_or_404(Trivia, id=trivia_id)).data},
                status=status.HTTP_201_CREATED,
        )        


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def user_voted_trivia(request):
    if request.method == "POST":
        voter = request.user
        pk = request.data.get("pk")
        trivia = get_object_or_404(Trivia, id=pk)
        if voter in trivia.voters.all():
            voted = True
            vote = Vote.objects.get(voter=voter, trivia=trivia).value
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


class CreateQuizView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (FormParser, MultiPartParser)
    serializer_class = QuizSerializer

    def create(self, request, *args, **kwargs):
        trivia_id = request.data.get("trivia_id")
        title = request.data.get("title")
        answer_one = request.data.get("answer_one")
        answer_two = request.data.get("answer_two")
        answer_three = request.data.get("answer_three")
        answer_four = request.data.get("answer_four")
        answer_five = request.data.get("answer_five")
        active_for = request.data.get("active_for")
        trivia = get_object_or_404(Trivia, id=trivia_id)
        author = request.user

        with transaction.atomic():
                quiz = Quiz.objects.create(
                    answer_one = answer_one,
                    answer_two = answer_two,
                    answer_three = answer_three,
                    title = title,
                    trivia = trivia,
                    answer_four = answer_four,
                    answer_five = answer_five,
                    active_for = active_for,
                    author=author,
                )      
        d = QuizSerializer(quiz).data
        return Response(d, status=status.HTTP_201_CREATED)


class QuizUpdateView(UpdateAPIView):
    lookup_field = "id"
    permission_classes = (IsAuthenticated,)
    parser_classes = (FormParser, MultiPartParser)
    serializer_class = QuizSerializer
    queryset = Quiz.objects.all()


class QuizDeleteView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self,request):
        data = request.data
        quiz = get_object_or_404(Quiz,id=data.get('quiz_id'))
        if quiz.author == request.user:
            quiz.delete()
            return Response({"success": "Quiz has been deleted"})


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def ListQuizOfTrivia(request):
    trivia_id = request.data.get("trivia_id")
    quiz = Quiz.objects.filter(
            trivia__id=trivia_id
        )
    paginator = CustomPagination()
    result_page = paginator.paginate_queryset(quiz,request)

    serializer = QuizSerializer(result_page, many=True, context={'request': request})
    return paginator.get_paginated_response({'data':serializer.data})    



class CreateCommentView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)
    serializer_class = CommentSerializer

    def create(self, request, *args, **kwargs):
        author = request.user
        trivia_id = request.data.get("trivia_id")
        text = request.data.get("text")
        parent_comment_id = request.data.get("parent_comment_id")
        trivia = get_object_or_404(Trivia, id=trivia_id)

        with transaction.atomic():
            comment = Comment.objects.create(
                trivia=trivia,
                author=author,
                parent_comment=parent_comment_id
                and Comment.objects.get(pk=parent_comment_id),
                text=text,
            )
            trivia.comments = trivia.comments + 1
            trivia.save()
        #if parent_comment_id and Comment.objects.get(pk=parent_comment_id):
           # Notification.objects.get_or_create(
              #  notification_type="C",
                #comment=Comment.objects.get(pk=parent_comment_id),
                #comments=(
                #    f"@{author.username} replied to your comment"
                #),
                #to_user=Comment.objects.get(pk=parent_comment_id).author,
                #from_user=author,
            #)
        #else:
            #Notification.objects.get_or_create(
                #notification_type="C",
                #trivia=trivia,
                #comments=(
                #    f"@{author.username} commented on your trivia"
                #),
                #to_user=trivia.author,
                #from_user=author,
            #) 

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

        try:
            vote = Vote.objects.get(voter=voter, comment=comment)
        except Vote.DoesNotExist:
            vote = Vote.objects.create(voter, value, comment=comment)
        else:
            if value == 1:
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


class ListNewCommentsOfTrivia(ListAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CommentSerializer_detailed
        if self.request.method == "POST":
            return CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(
            post__id=self.kwargs["t_id"]
        ).order_by("-created")


class ListOldCommentsOfTrivia(ListAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CommentSerializer_detailed
        if self.request.method == "POST":
            return CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(
            post__id=self.kwargs["t_id"]
        ).order_by("created")


class ListPopularCommentsOfTrivia(ListAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CommentSerializer_detailed
        if self.request.method == "POST":
            return CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(
            post__id=self.kwargs["t_id"]
        ).order_by("votes")


class DetailCommentsOfTrivia(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Comment.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CommentSerializer_detailed
        return CommentSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        conditions = {
            "trivia__id": self.kwargs["t_id"],
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
            "id": self.kwargs["s_id"],
        }
        return get_object_or_404(queryset, **conditions)

    def put(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)
