from django.contrib.auth.models import BaseUserManager
from django.db import models
from .sender import send_otp
from .querysets import OTPRequestQuerySet


class OTPManager(models.Manager):
    def get_queryset(self):
        return OTPRequestQuerySet(self.model, self._db)

    def is_valid(self, receiver, code):
        return self.get_queryset().is_valid(receiver, code)

    def generate(self, data):
        otp = self.model(channel=data['channel'], receiver=data['receiver'])
        otp.save(using=self._db)
        send_otp(otp)
        return otp
