from datetime import date
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework import status
from django.utils import timezone
from django.dispatch import receiver
from django.db import transaction
from django.db.models.signals import post_save
from django.shortcuts import get_object_or_404

from .models import Project


@receiver(post_save, sender=Project)
def post_save_project(sender, created, instance, **kwargs):    

    if created:
        project = instance
        creator = project.creator
        project.moderators.add(creator)
        project.subscribers.add(creator)
        project.subscriber_count =+ 1
        project.save()

