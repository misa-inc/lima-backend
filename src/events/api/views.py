from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction

from events.models import *
from directory.models import *
from page.models import *
from project.models import *

from events.api.serializers import *

from rest_framework import viewsets, status, generics
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
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

from account.api.serializers import UserSerializer
from events.models import Guest

from extensions.pagination import CustomPagination


# Create your views here.
class EventListAPIView(ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'is_active','type', 'location_type', 'virtual_type', 'city', 'country', 'state', 'county')
    pagination_class = CustomPagination

class EventAttendeesAPIView(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventAttendeesSerializer
    lookup_field = 'id'

class EventDetailView(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'is_active','type', 'location_type', 'virtual_type', 'city', 'country', 'state', 'county')

    def get_queryset(self):
        user = self.request.user
        return Event.objects.filter(owner=user.id)

    def perform_create(self, serializer):
        page_id = self.request.data.get("page_id")
        directory_id = self.request.data.get("directory_id")
        project_id = self.request.data.get("project_id")
        directory = get_object_or_404(Directory, id=directory_id)
        page = get_object_or_404(Page, id=page_id)
        project = get_object_or_404(Project, id=project_id)
        if page_id:
            serializer.save(owner=self.request.user, page=page)
        elif project_id:
            serializer.save(owner=self.request.user, project=project)           
        elif directory_id:
            serializer.save(owner=self.request.user, directory=directory)
        else:
            serializer.save(owner=self.request.user)


class FeedbackView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, event_id):
        event = Event.objects.get(id=event_id)
        if event.end_date < timezone.now() :
            guest =get_object_or_404(Event,event=event, user=request.user)
            serializer = UserSerializer(guest, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"success":serializer.data}, status=status.HTTP_200_OK)
            return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error":"Event not finished yet !"}, status=status.HTTP_400_BAD_REQUEST)

class FeedbackListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, event_id):
        user=request.user
        event = get_object_or_404(Event,owner=user,id=event_id)
        if event is None:
            return  Response({"error":"Event not created by you. !"}, status=status.HTTP_400_BAD_REQUEST)
        feedbacks = Guest.objects.filter(event=event)
        serializer = UserSerializer(feedbacks, many=True)
        return Response({"success":serializer.data}, status=status.HTTP_200_OK)

class EventWhoAttendeMe(ListAPIView):
    queryset=Event.objects.all()
    serializer_class=EventSerializer
    permission_classes=[IsAuthenticated,]

    def get_queryset(self):
        user = self.request.user
        guest_events = Guest.objects.filter(user=user)
        event_ids = [guest.event.id for guest in guest_events]
        queryset = Event.objects.filter(id__in=event_ids)
        return Response({"success":queryset}, status=status.HTTP_200_OK)


class JoinEventView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        if event.code_adhesion != request.data.get('code_adhesion'):
            return Response({"error": "Incorrect admission code."}, status=status.HTTP_400_BAD_REQUEST)
        guest, created = Guest.objects.get_or_create(event=event, user=request.user)
        return Response({"success": "Successfully joined event."}, status=status.HTTP_200_OK)


class ListRulesOfEvent(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RuleSerializer
    queryset = Rule.objects.all()

    def get(self, request, event_id):
        rule = Rule.objects.filter(id=event_id)
        serializer = RuleSerializer(rule, many=True)
        return Response(
            {
                "success": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class CreateRuleView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)
    serializer_class = RuleSerializer
    parser_classes = (FormParser, MultiPartParser)

    def create(self, request, *args, **kwargs):
        event_id = request.data.get("event_id")
        title = request.data.get("title")
        text = request.data.get("text")
        event = Event.objects.get(id=event_id)

        with transaction.atomic():
            rule = Rule.objects.create(event=event, text=text, title=title)
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


class ListPrizesOfEvent(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PrizeSerializer
    queryset = Prize.objects.all()

    def get(self, request, event_id):
        prize = Prize.objects.filter(id=event_id)
        serializer = PrizeSerializer(prize, many=True)
        return Response(
            {
                "success": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class CreatePrizeView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)
    serializer_class = PrizeSerializer
    parser_classes = (FormParser, MultiPartParser)

    def create(self, request, *args, **kwargs):
        event_id = request.data.get("event_id")
        title = request.data.get("title")
        image = request.data.get("image")
        url = request.data.get("url")
        event = Event.objects.get(id=event_id)

        with transaction.atomic():
            prize = Prize.objects.create(event=event, image=image, title=title, url=url)
        d = PrizeSerializer(prize).data
        return Response({
                "success": d.data,
            },
            status=status.HTTP_201_CREATED
        )


class PrizeDeleteView(DestroyAPIView):
    lookup_field = "id"
    permission_classes = (IsAuthenticated,)
    serializer_class = PrizeSerializer
    queryset = Prize.objects.all()


class ListAcknowledgementsOfEvent(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AcknowledgementSerializer
    queryset = Acknowledgement.objects.all()

    def get(self, request, event_id):
        acknowledgement = Acknowledgement.objects.filter(id=event_id)
        serializer = AcknowledgementSerializer(acknowledgement, many=True)
        return Response(
            {
                "success": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class CreateAcknowledgementView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)
    serializer_class = AcknowledgementSerializer
    parser_classes = (FormParser, MultiPartParser)

    def create(self, request, *args, **kwargs):
        event_id = request.data.get("event_id")
        title = request.data.get("title")
        image = request.data.get("image")
        url = request.data.get("url")
        event = Event.objects.get(id=event_id)

        with transaction.atomic():
            acknowledgement = Acknowledgement.objects.create(event=event, image=image, title=title, url=url)
        d = AcknowledgementSerializer(acknowledgement).data
        return Response({
                "success": d.data,
            },
            status=status.HTTP_201_CREATED
        )


class AcknowledgementDeleteView(DestroyAPIView):
    lookup_field = "id"
    permission_classes = (IsAuthenticated,)
    serializer_class = AcknowledgementSerializer
    queryset = Acknowledgement.objects.all()


class ListStepsOfEvent(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = StepSerializer
    queryset = Step.objects.all()

    def get(self, request, event_id):
        step = Step.objects.filter(id=event_id)
        serializer = StepSerializer(step, many=True)
        return Response(
            {
                "success": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class CreateStepView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)
    serializer_class = StepSerializer
    parser_classes = (FormParser, MultiPartParser)

    def create(self, request, *args, **kwargs):
        event_id = request.data.get("event_id")
        title = request.data.get("title")
        image = request.data.get("image")
        url = request.data.get("url")
        event = Event.objects.get(id=event_id)

        with transaction.atomic():
            step = Step.objects.create(event=event, image=image, title=title, url=url)
        d = StepSerializer(step).data
        return Response({
                "success": d.data,
            },
            status=status.HTTP_201_CREATED
        )


class StepDeleteView(DestroyAPIView):
    lookup_field = "id"
    permission_classes = (IsAuthenticated,)
    serializer_class = StepSerializer
    queryset = Step.objects.all()
    