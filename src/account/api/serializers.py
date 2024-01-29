from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from taggit.serializers import (TagListSerializerField,
                                TaggitSerializer)

from account.models import *



class GetTwoStepPasswordSerializer(serializers.Serializer):
    """
        Base serializer two-step-password.
    """
    password = serializers.CharField(
        max_length=20,
    )

    confirm_password = serializers.CharField(
        max_length=20,
    )

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError(
                {"error": "Your passwords didn't match."}
            )

        return data


class ChangeTwoStepPasswordSerializer(GetTwoStepPasswordSerializer):
    old_password = serializers.CharField(
        max_length=20,
    )


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    default_error_messages = {
        "error": "The username should only contain alphanumeric characters"
    }

    class Meta:
        model = User
        fields = ["email", "username", "password"]

    def validate(self, attrs):
        email = attrs.get("email", "")
        username = attrs.get("username", "")

        if not username.isalnum():
            raise serializers.ValidationError(self.default_error_messages)
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class VerifyOTPRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.IntegerField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "otp", "tokens", "username", "slug" ]

    def validate(self, attrs):
        email = attrs.get("email", "")
        otp = attrs.get("otp", "")

        user = User.objects.filter(email=email).first()
        refresh = RefreshToken.for_user(user=user)
        refresh_token = str(refresh)
        access_token = str(refresh.access_token)

        if not user.is_active:
            raise AuthenticationFailed("Account has been disabled")   
        if user.otp != otp:
            raise AuthenticationFailed("The OTP Code is invalid")                             

        return {"id": user.id, "email": user.email, "username":user.username, "slug": user.slug, "tokens": user.tokens, "refresh_token": refresh_token, "access_token": access_token}


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "tokens"]

    def validate(self, attrs):
        email = attrs.get("email", "")
        password = attrs.get("password", "")

        user = User.objects.filter(email=email).first()

        if not user or not user.check_password(password):
            raise AuthenticationFailed("Invalid credentials, try again")
        if not user.is_active:
            raise AuthenticationFailed("Account has been disabled")
                                

        return {"email": user.email}


class VerifyOTPLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.IntegerField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "otp", "tokens", "username", "slug" ]

    def validate(self, attrs):
        email = attrs.get("email", "")
        otp = attrs.get("otp", "")

        user = User.objects.filter(email=email).first()
        refresh = RefreshToken.for_user(user=user)
        refresh_token = str(refresh)
        access_token = str(refresh.access_token)

        if not user.is_active:
            raise AuthenticationFailed("Account has been disabled")                            
        if user.otp != otp:
            raise AuthenticationFailed("The OTP Code is invalid")                             
        
        return {"id": user.id, "email": user.email, "username":user.username, "slug": user.slug, "tokens": user.tokens, "refresh_token": refresh_token, "access_token": access_token}



class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ["email"]


class VerifyOTPResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.IntegerField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "otp", "username", "slug" ]

    def validate(self, attrs):
        email = attrs.get("email", "")
        otp = attrs.get("otp", "")

        user = User.objects.filter(email=email).first()

        if not user.is_active:
            raise AuthenticationFailed("Account has been disabled")                            
        if user.otp != otp:
            raise AuthenticationFailed("The OTP Code is invalid")                             

        return {"id": user.id, "email": user.email, "username":user.username, "slug": user.slug}



class ResendEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ["email"]

    def validate(self, attrs):
        email = attrs.get("email", "")
        
        user = User.objects.filter(email=email).first()

        if not user.is_active:
            raise AuthenticationFailed("Account has been disabled")
        return attrs


class SetNewPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)
    password = serializers.CharField(min_length=6, max_length=68, write_only=True)

    class Meta:
        fields = ["email", "password"]

    def validate(self, attrs):
        try:
            email = attrs.get("email")
            password = attrs.get("password")

            user = User.objects.filter(email=email).first()
            user.set_password(password)
            user.save()

            return user
        except Exception as e:
            raise AuthenticationFailed("The otp is invalid", 401)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {"bad_token": ("Token is expired or invalid")}

    def validate(self, attrs):
        self.token = attrs["refresh"]
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail("bad_token")


class UserSerializer(TaggitSerializer, serializers.HyperlinkedModelSerializer):
    tags = TagListSerializerField(default=[])

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "full_name", 
            "tags",
            "headline",
            "call_code",
            "phone",
            "author",
            "bio",
            "sex",
            "avatar",
            "cover",
            "website",
            "country",
            "state",
            "address",
            "city",
            "location",
            "two_step_password",
            "day",
            "month",
            "year",
            "dob",
            "address",
            "city",
            "state",
            "otp",
            "push_token",
            "friends_count",
            "friends",
            "blocked_count",
            "blocked",
            "is_page_member",
            "is_page_moderator",
            "is_organization_member",
            "is_organization_moderator",
            "is_directory_member",
            "is_directory_moderator",
            "is_group_member",
            "is_group_moderator",
            "is_project_member",
            "is_project_moderator",
            "is_verified",
            "is_active",
            "active",
            "is_staff",
            "is_admin",
            "is_banned",
            "is_deleted",
            "tos",
            "slug",
            "created",
            "created_at",
        )


class UserCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "friends_count",
            "blocked_count"
            )

class UserLessInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "full_name",  "avatar", "bio"]


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = "__all__"


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = "__all__"


class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = "__all__"


class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = "__all__"


class UserProfileSerializer(TaggitSerializer, serializers.ModelSerializer):

    friends_count = serializers.ReadOnlyField()
    blocked_count = serializers.ReadOnlyField()
    is_self = serializers.SerializerMethodField()
    blocked = serializers.SerializerMethodField()
    tags = TagListSerializerField(default=[])

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "full_name", 
            "headline",
            "call_code",
            "tags",
            "phone",
            "author",
            "bio",
            "sex",
            "avatar",
            "cover",
            "website",
            "country",
            "state",
            "address",
            "city",
            "location",
            "day",
            "month",
            "year",
            "dob",
            "otp",
            "two_step_password",
            "friends_count",
            "friends",
            "blocked_count",
            "blocked",
            "is_page_member",
            "is_page_moderator",
            "is_organization_member",
            "is_organization_moderator",
            "is_directory_member",
            "is_directory_moderator",
            "is_group_member",
            "is_group_moderator",
            "is_project_member",
            "is_project_moderator",
            "is_verified",
            "is_active",
            "active",
            "is_staff",
            "is_admin",
            "is_banned",
            "is_deleted",
            "slug",
            "tos",
            "is_self",
            "created",
            "created_at",
        )

    def get_is_self(self, user):
        if "request" in self.context:
            request = self.context["request"]
            if user.id == request.user.id:
                return True
            else:
                return False
        return False

    def get_blocked(self, obj):
        if "request" in self.context:
            request = self.context["request"]
            if obj in request.user.blocked.all():
                return True
        return False


class ListUserSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField(default=[])

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "full_name", 
            "headline",
            "tags",
            "call_code",
            "author",
            "phone",
            "bio",
            "sex",
            "avatar",
            "cover",
            "website",
            "country",
            "state",
            "address",
            "city",
            "location",
            "day",
            "month",
            "year",
            "dob",
            "otp",
            "two_step_password",
            "friends_count",
            "friends",
            "blocked_count",
            "blocked",
            "is_verified",
            "is_active",
            "active",
            "is_staff",
            "is_admin",
            "is_banned",
            "is_deleted",
            "slug",
            "tos",
            "tokens",
            "created",
            "created_at",
        )
        depth=1