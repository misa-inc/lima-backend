from django.core.cache import cache
from django.conf import settings

from rest_framework.response import Response
from rest_framework import status

from extensions.utils import otp_generator, get_client_ip
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import get_template

import random
from extensions.utils import Util
from account.models import User

# send otp code


def send_otp(request, phone, email):
    if phone:
        otp = otp_generator()
        ip = get_client_ip(request)
        cache.set(f"{ip}-for-authentication", phone, settings.EXPIRY_TIME_OTP)
        cache.set(phone, otp, settings.EXPIRY_TIME_OTP)

        # TODO Here the otp code must later be sent to the user's phone number by SMS system.
        # But in debug mode we return the otp code.

        context = {
            "otp": f"{otp}",
        }
        return Response(
            context,
            status=status.HTTP_200_OK,
        )
    elif email:
        subject = "Account Verification Email From Pyramid"
        otp = otp_generator()
        ip = get_client_ip(request)
        cache.set(f"{ip}-for-authentication", email, settings.EXPIRY_TIME_OTP)
        cache.set(email, otp, settings.EXPIRY_TIME_OTP)
        message = f"Your OTP is {otp}"
        email_from = settings.EMAIL_HOST
        send_mail(subject,message, email_from,[email])
        user_obj = User.objects.get(email=email)
        user_obj.otp = otp
        user_obj.save()
        context = {
            "otp": f"{otp}",
        }
        return Response(
            context,
            status=status.HTTP_200_OK,
        )
    else:
        context = {
            "error": f"Input an email or phone number...",
        }
        return Response(
            context,
            status=status.HTTP_400_BAD_REQUEST,
        )
