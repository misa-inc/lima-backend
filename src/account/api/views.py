import os
import random
from datetime import date

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.core.cache import cache
from django.template.loader import get_template

from rest_framework import generics, status, permissions
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes

from .serializers import (
    ListUserSerializer,
    UserProfileSerializer,
    UserProfileSerializer,
    RegisterSerializer,
    LogoutSerializer,
    LoginSerializer,
    VerifyOTPRegisterSerializer,
    VerifyOTPLoginSerializer,
    VerifyOTPResetSerializer,
    ResendEmailSerializer,
    SetNewPasswordSerializer,
    ResetPasswordSerializer,
    ChangeTwoStepPasswordSerializer,
    GetTwoStepPasswordSerializer,
)
from account.models import User
from extensions.utils import get_client_ip, Util
from extensions.permissions import IsSuperUser
from notifications.models import Notification




class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        user_data = {}

        if serializer.is_valid():
            serializer.save()
            user_data = serializer.data
            otp = random.randint(100000, 999999)
            user = User.objects.get(email=user_data["email"])
            user.otp = otp
            now = date.today()
            user.day = now.day
            #user.month = now.month
            user.year = now.year
            call_code = request.data.get("call_code")
            phone = request.data.get("phone")
            user.phone = phone
            user.call_code = call_code
            user.is_active = True
            user.tos = True

            user_data["email"] = user.email
            user_data["username"] = user.username
            html_tpl_path = "email_templates/welcome.html"
            html_intro_path = "email_templates/intro.html"
            context_data = {"name": user.username, "code": user.otp}
            email_html_template = get_template(html_tpl_path).render(context_data)
            intro_html_template = get_template(html_intro_path).render(context_data)
            data = {
                "email_body": email_html_template,
                "to_email": user.email,
                "email_subject": "Please verify your Lima email",
            }
            intro = {
                "email_body": intro_html_template,
                "to_email": user.email,
                "email_subject": "Welcome To Lima",
            }
            Util.send_email(data)
            Util.send_email(intro)
            user.save()
            return Response(user_data, status=status.HTTP_201_CREATED)

        else:

            return Response(
                {"error": "The username is already taken"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ResendRegisterEmailView(generics.GenericAPIView):
    serializer_class = ResendEmailSerializer

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = ResendEmailSerializer(data=request.data)
        user_data = {}

        if serializer.is_valid():
            user_data = serializer.data
            otp = random.randint(100000, 999999)
            user = User.objects.get(email=user_data["email"])
            user.otp = 0
            user.otp = otp
            user.save()
            user_data["email"] = user.email
            html_tpl_path = "email_templates/welcome.html"
            context_data = {"name": user.username, "code": user.otp}
            email_html_template = get_template(html_tpl_path).render(context_data)
            data = {
                "email_body": email_html_template,
                "to_email": user.email,
                "email_subject": "Please verify your Lima email",
            }

            Util.send_email(data)
            return Response(user_data, status=status.HTTP_201_CREATED)

        else:

            return Response(
                {"error": "There was an error, try again or reach out to support."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class VerifyEmail(generics.GenericAPIView):
    serializer_class = VerifyOTPRegisterSerializer

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = VerifyOTPRegisterSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.data["email"]
            user = User.objects.get(email=email)
            refresh = RefreshToken.for_user(user=user)
            refresh_token = str(refresh)
            access_token = str(refresh.access_token)
            user.is_verified = True
            user.is_active = True
            user.active = True
            user.otp = 0
            user.save()
            return Response(
                {
                    "id": user.id,
                    "email": user.email,
                    "username": user.username,
                    "phone": user.phone,
                    "slug": user.slug,
                    "refresh_token": refresh_token,
                    "access_token": access_token,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response({"error": "The OTP code is invalid"}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.data
        user = User.objects.get(email=user_data["email"])
        if user.is_deleted:
            otp = random.randint(100000, 999999)
            user.otp = otp
            user.is_verified = True
            user.save()
            html_tpl_path = "email_templates/login.html"
            context_data = {"name": user.username, "code": user.otp}
            email_html_template = get_template(html_tpl_path).render(context_data)
            data = {
                "email_body": email_html_template,
                "to_email": user.email,
                "email_subject": "Lima login verification",
            }

            Util.send_email(data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error":"User does not exist"}, status=status.HTTP_400_BAD_REQUEST)


class ResendLoginEmailView(generics.GenericAPIView):
    serializer_class = ResendEmailSerializer

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = ResendEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.data
        user = User.objects.get(email=user_data["email"])
        if user.is_deleted:
            otp = random.randint(100000, 999999)
            user.otp = 0
            user.otp = otp
            user.is_verified = True
            user.save()
            html_tpl_path = "email_templates/login.html"
            context_data = {"name": user.username, "code": user.otp}
            email_html_template = get_template(html_tpl_path).render(context_data)
            data = {
                "email_body": email_html_template,
                "to_email": user.email,
                "email_subject": "Lima login verification",
            }

            Util.send_email(data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error":"User does not exist"}, status=status.HTTP_400_BAD_REQUEST)


class VerifyLoginEmail(generics.GenericAPIView):
    serializer_class = VerifyOTPLoginSerializer

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = VerifyOTPLoginSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            email = serializer.data["email"]
            user = User.objects.get(email=email)
            refresh = RefreshToken.for_user(user=user)
            refresh_token = str(refresh)
            access_token = str(refresh.access_token)
            user.active = True
            user.otp = 0
            user.save()
            return Response(
                {
                    "id": user.id,
                    "email": user.email,
                    "username": user.username,
                    "phone": user.phone,
                    "slug": user.slug,
                    "refresh_token": refresh_token,
                    "access_token": access_token,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response({"error": "The OTP code is invalid"}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordAPIView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.data
        user = User.objects.filter(email=user_data["email"]).first()
        if user and user.is_active:
            otp = random.randint(100000, 999999)
            user.otp = otp
            user.save()
            html_tpl_path = "email_templates/reset.html"
            context_data = {"name": user.username, "code": user.otp}
            email_html_template = get_template(html_tpl_path).render(context_data)
            data = {
                "email_body": email_html_template,
                "to_email": user.email,
                "email_subject": "Lima reset password verification",
            }

            Util.send_email(data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "There was an error, try again or reach out to support."}, status=status.HTTP_400_BAD_REQUEST)


class ResendResetPasswordView(generics.GenericAPIView):
    serializer_class = ResendEmailSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = ResendEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.data
        user = User.objects.filter(email=user_data["email"]).first()
        if user and user.is_active:
            otp = random.randint(100000, 999999)
            user.otp = otp
            user.save()
            html_tpl_path = "email_templates/reset.html"
            context_data = {"name": user.username, "code": user.otp}
            email_html_template = get_template(html_tpl_path).render(context_data)
            data = {
                "email_body": email_html_template,
                "to_email": user.email,
                "email_subject": "Lima reset password verification",
            }

            Util.send_email(data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "There was an error, try again or reach out to support."}, status=status.HTTP_400_BAD_REQUEST)


class VerifyResetEmail(generics.GenericAPIView):
    serializer_class = VerifyOTPResetSerializer

    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = VerifyOTPResetSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            email = serializer.data["email"]
            user = User.objects.get(email=email)
            user.active = True
            user.otp = 0
            user.save()
            return Response(
                {
                    "id": user.id,
                    "email": user.email,
                    "username": user.username,
                    "slug": user.slug,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response({"error": "The OTP code is invalid"}, status=status.HTTP_400_BAD_REQUEST)


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    permission_classes = (permissions.AllowAny,)

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {"success": "Password reset successful"},
            status=status.HTTP_200_OK,
        )


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(id=user_data["id"])
        if user.is_verified:
            user.active = False
            user.otp = 0
            user.save()

        return Response({"success": "Logged out successfully"}, status=status.HTTP_204_NO_CONTENT)


class UserFriends(APIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ListUserSerializer

    def get(self, username):

        try:
            found_user = User.objects.get(username=username)
            print(f"found user {found_user}")
        except User.DoesNotExist:
            return Response({"error":"User not found"},status=status.HTTP_404_NOT_FOUND)

        user_friends = found_user.friends.all()
        serializer = self.serializer_class(user_friends, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UserBlocked(APIView):
    def get(self, request, username):

        try:
            found_user = User.objects.get(username=username)
            print(f"found user {found_user}")
        except User.DoesNotExist:
            return Response({"error":"User not found"}, status=status.HTTP_404_NOT_FOUND)

        user_blocked = found_user.blocked.all()
        serializer = ListUserSerializer(
            user_blocked, many=True, context={"request": request}
        )

        return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def befriend_user(request):
    if request.method == "POST":
        username = request.data.get("username")
        fu_user = get_object_or_404(User, username=username)
        user = request.user

        if fu_user in user.friends.all():
            friends = False
            user.friends.remove(fu_user)
            user.save()
            fu_user.friends.remove(user)
            fu_user.save()

            Notification.objects.get_or_create(
                notification_type="UF",
                comments=(f"@{user.username} removed you from his friends list"),
                to_user=fu_user,
                from_user=user,
            )
        else:
            friends = True

            Notification.objects.get_or_create(
                notification_type="F",
                comments=(f"@{user.username} sent you a friend request"),
                to_user=fu_user,
                from_user=user,
            )
        return Response(
            {
                "friends": friends,
            },
            status=status.HTTP_201_CREATED,
        )
    return Response(
        {
            "error": "An error occurred, try again later",
        },
        status=status.HTTP_400_BAD_REQUEST,
    )



@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def accept_decline_friend_request(request):
    if request.method == "POST":
        username = request.data.get("username")
        status = request.data.get("status")
        fu_user = get_object_or_404(User, username=username)
        user = request.user

        if status == "DECLINED":
            friends = False

            Notification.objects.get_or_create(
                notification_type="UF",
                comments=(f"@{user.username} declined your friend request"),
                to_user=fu_user,
                from_user=user,
            )
        else:
            friends = True
            fu_user.friends.add(user)
            fu_user.save()
            user.friends.add(user)
            user.save()

            Notification.objects.get_or_create(
                notification_type="F",
                comments=(f"@{user.username} accepted your friend request"),
                to_user=fu_user,
                from_user=user,
            )
        return Response(
            {
                "friends": friends,
            },
            status=status.HTTP_201_CREATED,
        )
    return Response(
        {
            "error": "An error occurred, try again later",
        },
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def user_befriended_user(request):
    if request.method == "POST":
        username = request.data.get("username")
        fu_user = get_object_or_404(User, username=username)
        user = request.user
        if user in fu_user.friends.all():
            friends = True
        else:
            friends = False
        return Response(
            {
                "friends": friends,
            },
            status=status.HTTP_201_CREATED,
        )
    return Response(
        {
            "error": "An error occurred, try again later",
        },
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def block_user(request):
    if request.method == "POST":
        username = request.data.get("username")
        to_be_blocked_user = get_object_or_404(User, username=username)
        user = request.user

        blocked = True
        user.blocked.add(to_be_blocked_user)
        user.save()

        return Response(
            {
                "blocked": blocked,
            },
            status=status.HTTP_201_CREATED,
        )
    return Response(
        {
            "error": "An error occurred, try again later",
        },
        status=status.HTTP_400_BAD_REQUEST,
    )


class UserDetailView(RetrieveAPIView):
    lookup_field = "username"
    permission_classes = (IsAuthenticated,)
    serializer_class = ListUserSerializer
    queryset = User.objects.all()


class UserUpdateView(UpdateAPIView):
    lookup_field = "username"
    permission_classes = (IsAuthenticated,)
    serializer_class = ListUserSerializer
    queryset = User.objects.all()
    parser_classes = (FormParser, MultiPartParser)


class UpdateUserView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def put(self, request, username):
        user = get_object_or_404(User, username=username)
        users_serializer = ListUserSerializer(user, data=request.data)
        if users_serializer.is_valid():
            users_serializer.save()
            return Response(users_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(users_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, username):
        user = get_object_or_404(User, username=username)
        users_serializer = ListUserSerializer(user, data=request.data)
        if users_serializer.is_valid():
            users_serializer.save()
            return Response(users_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(users_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, username):
        user = get_object_or_404(User, username=username)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserDeleteView(DestroyAPIView):
    lookup_field = "username"
    permission_classes = (IsAuthenticated,)
    serializer_class = ListUserSerializer
    queryset = User.objects.all()


class ChangePassword(APIView):
    def put(self, request, username, format=None):

        user = request.user

        if user.username == username:

            current_password = request.data.get("current_password", None)

            if current_password is not None:

                passwords_match = user.check_password(current_password)

                if passwords_match:

                    new_password = request.data.get("new_password", None)

                    if new_password is not None:

                        user.set_password(new_password)

                        user.save()

                        return Response(
                                       {
                                        "success": "Successfully changed password",
                                        },
                                        status=status.HTTP_200_OK
                                    )

                    else:

                        return Response(
                                {
                                    "error": "Enter a new password",
                                },
                                status=status.HTTP_400_BAD_REQUEST
                            )

                else:

                    return Response(
                        {
                            "error": "Enter the correct password, don't remember the password, reach out to support",
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

            else:

                return Response(
                    {
                        "error": "Enter your current password",
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        else:

            return Response(
                {
                    "error": "Can't change password of another user",
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class VerifyTwoStepPassword(APIView):
    """
    post:
        Send two-step-password to verify and complete authentication.

        parameters: [password, confirm_password,]
    """

    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request):
        serializer = GetTwoStepPasswordSerializer(data=request.data)
        if serializer.is_valid():
            ip = get_client_ip(request)
            user = cache.get(f"{ip}-for-two-step-password")
            
            if user is not None:
                password = serializer.data.get("password")
                check_password: bool = user.check_password(password)

                if check_password:
                    refresh = RefreshToken.for_user(user)
                    cache.delete(f"{ip}-for-two-step-password")

                    context = {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    }
                    return Response(
                        context,
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        {
                            "error": "The password entered is incorrect",
                        },
                        status=status.HTTP_406_NOT_ACCEPTABLE,
                    )
            return Response(
                {
                    "error": "The two-step-password entry time has elapsed",
                },
                status=status.HTTP_408_REQUEST_TIMEOUT,
            )
        else:
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST,
            )


class CreateTwoStepPassword(APIView):
    """
    post:
        Send a password to create a two-step-password.
        
        parameters: [new_password, confirm_new_password]
    """

    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request):
        if not request.user.two_step_password:
            serializer = GetTwoStepPasswordSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            new_password = serializer.data.get("password")

            try:
                _: None = validate_password(new_password)
            except ValidationError as err:
                return Response(
                    {"errors":err},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            user = get_object_or_404(
                User,
                slug=request.user.slug,
            )
            user.set_password(new_password)
            user.two_step_password = True
            user.save(update_fields=["password", "two_step_password"])     
            return Response(
                {
                    "success":"Your password was changed successfully.",
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {
                "error":"Your request could not be approved.",
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )


class ChangeTwoStepPassword(APIView):
    """
    post:
        Send a password to change a two-step-password.
        
        parameters: [old_password, new_password, confirm_new_password,]
    """

    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request):
        if request.user.two_step_password:
            serializer = ChangeTwoStepPasswordSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            new_password = serializer.data.get("password")

            try:
                _: None = validate_password(new_password)
            except ValidationError as err:
                return Response(
                    {"errors":err},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            old_password = serializer.data.get("old_password")
            user = get_object_or_404(
                User, 
                slug=request.user.slug,
            )
            check_password: bool = user.check_password(old_password)

            if check_password:
                user.set_password(new_password)
                user.save(update_fields=["password"])

                return Response(
                    {
                        "success":"Your password was changed successfully.",
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "error":"The password entered is incorrect.",
                    },
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )

        return Response(
            {
                "error":"Your request could not be approved.",
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )


class DeleteAccount(APIView):
    """
    delete:
        Delete an existing User instance.
    """
    
    permission_classes = [
        IsAuthenticated,
    ]

    def delete(self, request):
        user = User.objects.get(slug=request.user.slug)
        if not request.user.two_step_password:
            user.is_deleted=True
            user.save()
            return Response(
                {
                    "Removed successfully.": "Your account has been successfully deleted.",
                },
                status=status.HTTP_204_NO_CONTENT,
            )
        else:
            serializer = GetTwoStepPasswordSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            password = serializer.data.get("password")
            check_password: bool = user.check_password(password)

            if check_password:
                user.is_deleted=True
                user.save()

                return Response(
                    {
                        "Removed successfully.": "Your account has been successfully deleted.",
                    },
                    status=status.HTTP_204_NO_CONTENT,
                )
            else:
                return Response(
                    {
                        "error": "The password entered is incorrect.",
                    },
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )