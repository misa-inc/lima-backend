from datetime import date
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework import status
from django.utils import timezone
from django.dispatch import receiver
from django.db import transaction
from django.db.models.signals import post_save
from django.shortcuts import get_object_or_404

from .models import Directory


@receiver(post_save, sender=Directory)
def post_save_directory(sender, created, instance, **kwargs):    
    if created:
        directory = instance
        creator = directory.creator
        directory.moderators.add(creator)
        directory.subscribers.add(creator)
        directory.subscriber_count =+ 1
        directory.save()

