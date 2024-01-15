from django.urls import path
from rest_framework import routers


from .views import *

router = routers.SimpleRouter()
router.register('myevent', EventViewSet, basename='event')


urlpatterns=[
    path("join/event/<int:event_id>",JoinEventView.as_view(),name="join_event"),
    path("myfeedback/<int:event_id>",FeedbackView.as_view(),name="myfeedback"),
    path("myevent/getfeedbacks/<int:event_id>",FeedbackListView.as_view(),name="list_feedbacks"),
    path("event_list",EventListAPIView.as_view(),name="list_event_public"),
    path("all_attendes/<int:id>",EventAttendeesAPIView.as_view(),name="list_attendees"),
    path("detail_event/<int:pk>",EventDetailView.as_view(),name="detail_event"),
    path('event_list_guest',EventWhoAttendeMe.as_view(),name="list_event_guest"),
    path('event/create/rule/', CreateRuleView.as_view(), name='create_rule'), 
    path('event/rule/<int:id>/delete/', RuleDeleteView.as_view(), name='delete_rule'),
    path('event/<int:event_id>/rules/', ListRulesOfEvent.as_view(), name='events_rules'),
    path('event/create/acknowledgement/', CreateAcknowledgementView.as_view(), name='create_acknowledgement'), 
    path('event/acknowledgement/<int:id>/delete/', AcknowledgementDeleteView.as_view(), name='delete_acknowledgement'),
    path('event/<int:event_id>/acknowledgements/', ListAcknowledgementsOfEvent.as_view(), name='events_acknowledgements'),
    path('event/create/prize/', CreatePrizeView.as_view(), name='create_prize'), 
    path('event/prize/<int:id>/delete/', PrizeDeleteView.as_view(), name='delete_prize'),
    path('event/<int:event_id>/prizes/', ListPrizesOfEvent.as_view(), name='events_prizes'),
    path('event/create/step/', CreateStepView.as_view(), name='create_step'), 
    path('event/step/<int:id>/delete/', StepDeleteView.as_view(), name='delete_step'),
    path('event/<int:event_id>/steps/', ListStepsOfEvent.as_view(), name='events_steps'),
]

urlpatterns +=router.urls