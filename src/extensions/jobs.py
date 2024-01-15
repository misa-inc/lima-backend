from django.utils import timezone

#from events.models import Event


def test():
    print("ho")


def survey_event():
    now = timezone.now()
    #events = Event.objects.filter(end_date_inscription__lt=now, status='ACTIVE')
    #for event in events:
        #event.status = 'CLOSED'
        #event.save()
