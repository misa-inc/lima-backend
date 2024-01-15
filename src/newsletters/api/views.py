from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    UpdateAPIView,
    RetrieveAPIView,
    DestroyAPIView,
)

from django.db import transaction
from django.shortcuts import render, get_object_or_404

from newsletters.models import Newsletter, Article
from account.models import User
from .serializers import NewsletterSerializer, ArticleSerializer
from account.api.serializers import UserSerializer
from extensions.permissions import IsOwner
from extensions.utils import Util
from extensions.pagination import CustomPagination

from rest_framework.permissions import (
    AllowAny,
)


class NewslettersViewSet(viewsets.ModelViewSet):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer
    permission_classes = (AllowAny,)


    def create(self, request, *args, **kwargs):
        user = User.objects.get(id=request.data['owner'])

        if user:
            newsletter = NewsletterSerializer(data=request.data)
            if newsletter.is_valid():
                newsletter.save()
                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST, data=newsletter.errors)
        else:
            return Response({"mensaje": "Owner no es administrador"}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['GET'], detail=True)
    def owner(self, req, pk=None):
        newsletter = self.get_object()
        serializer = UserSerializer(newsletter.owner)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(methods=['GET', 'POST', 'DELETE'], detail=True)
    def suscriptions(self, req, pk=None):
        newsletter = self.get_object()

        if req.method == 'GET':
            serializer = UserSerializer(newsletter.subscribers, many=True)
            return Response(status=status.HTTP_200_OK, data=serializer.data)

        if req.method in ['POST', 'DELETE']:
            users_id = req.data['users']
            for id in users_id:
                user = User.objects.get(id=id)
                if req.method == 'POST':
                    newsletter.subscribers.add(user)
                    #TODO improve this later
                    email_body = 'Hello ' + user.username + ' welcome to \n' + newsletter.name
                    data = {'email_body': email_body,
                            'to_email': user.email,
                            'email_subject': 'Subscription'}

                    Util.send_email(data)
                    serializer = UserSerializer(newsletter.subscribers, many=True)
                    return Response(status=status.HTTP_201_CREATED, data=serializer.data)
                elif req.method == 'DELETE':
                    newsletter.subscribers.remove(user)
                    serializer = UserSerializer(newsletter.subscribers, many=True)
                    return Response(status=status.HTTP_204_NO_CONTENT, data=serializer.data)

    @action(methods=['GET', 'POST', 'DELETE'], detail=True)
    def target(self, req, pk=None):
        newsletter = self.get_object()
        target = newsletter.target.count()
        if req.method == 'GET':
            serializer = UserSerializer(newsletter.target, many=True)
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        #The will be an engine which will add users automatically to a newsletter as being targets, 
        # and will be setup based on their likes, what the view, and other metrics on the platform, 
        # as it will add users as being targets, which will be seen on the frontend as a way to turn them into subscribers
        if req.method in ['POST', 'DELETE']:
            users_id = req.data['users']
            for id in users_id:
                user = User.objects.get(id=int(id))
                if req.method == 'POST':
                    newsletter.target.add(user)

                    serializer = UserSerializer(newsletter.target, many=True)
                    return Response(status=status.HTTP_201_CREATED, data=serializer.data)
                elif req.method == 'DELETE':
                    newsletter.target.remove(user)
                    serializer = UserSerializer(newsletter.target, many=True)
                    return Response(status=status.HTTP_204_NO_CONTENT, data=serializer.data)


class NewsletterDetailView(RetrieveAPIView):
    lookup_field = "name"
    permission_classes = (AllowAny,)
    serializer_class = NewsletterSerializer
    queryset = Newsletter.objects.all()


class NewsletterUpdateView(UpdateAPIView):
    lookup_field = "name"
    permission_classes = (AllowAny,)
    serializer_class = NewsletterSerializer
    queryset = Newsletter.objects.all()
    parser_classes = (FormParser, MultiPartParser)


class NewsletterDeleteView(DestroyAPIView):
    lookup_field = "name"
    permission_classes = (AllowAny,)
    serializer_class = NewsletterSerializer
    queryset = Newsletter.objects.all()


@api_view(["POST"])
@permission_classes((AllowAny,))
def user_creator_newsletter(request):
    if request.method == "POST":
        pk = request.data.get("pk")
        newsletter = get_object_or_404(Newsletter, id=pk)
        if request.user is newsletter.owner:
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
@permission_classes((AllowAny,))
def user_joined_newsletter(request):
    if request.method == "POST":
        pk = request.data.get("pk")
        newsletter = get_object_or_404(Newsletter, id=pk)
        if request.user in newsletter.subscribers.all():
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
@permission_classes((AllowAny,))
def join_newsletter(request):
    if request.method == "POST":
        pk = request.data.get("pk")
        newsletter = get_object_or_404(Newsletter, id=pk)
        if request.user in newsletter.subscribers.all():
            joined = False
            newsletter.subscribers.remove(request.user)
            newsletter.save()
        else:
            joined = True
            newsletter.subscribers.add(request.user)
            newsletter.save()
        return Response(
            {
                "joined": joined,
            },
            status=status.HTTP_201_CREATED,
        )


class ListUserCreatedNewletter(ListAPIView):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        my_newsletters = Newsletter.objects.filter(owner=self.request.user.id)
        return my_newsletters


class ListUserSubscribedNewletter(ListAPIView):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        my_subscritions = Newsletter.objects.filter(subscribers=self.request.user.id)
        return my_subscritions


@api_view(['GET'])
@permission_classes((AllowAny,))
def ListArticlesOfNewsletter(request, name):
    article = Article.objects.filter(newsletter__name=name)
    paginator = CustomPagination()
    result_page = paginator.paginate_queryset(article,request)

    serializer = ArticleSerializer(result_page, many=True, context={'request': request})
    return paginator.get_paginated_response({'data':serializer.data}) 


class CreateArticleView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ArticleSerializer
    parser_classes = (FormParser, MultiPartParser)

    def create(self, request, *args, **kwargs):
        cover = request.data.get("cover")
        name = request.data.get("name")
        content = request.data.get("content")
        newsletter_name = request.data.get("newsletter_name")
        newsletter = get_object_or_404(Newsletter, name=newsletter_name)

        #TODO add the functionality of communicating with subscribers via InMail and Email that a new article has been created
        with transaction.atomic():
            article = Article.objects.create(
                newsletter=newsletter, 
                name=name, 
                content=content, 
                cover=cover
            )
        d = ArticleSerializer(article).data
        return Response(d, status=status.HTTP_201_CREATED)


class ArticleDetailView(RetrieveAPIView):
    lookup_field = "name"
    permission_classes = (AllowAny,)
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()


class ArticleUpdateView(UpdateAPIView):
    lookup_field = "name"
    permission_classes = (AllowAny,)
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    parser_classes = (FormParser, MultiPartParser)


class ArticleDeleteView(DestroyAPIView):
    lookup_field = "name"
    permission_classes = (AllowAny,)
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
