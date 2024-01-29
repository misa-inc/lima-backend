from rest_framework import serializers
from page.models import *
from taggit.serializers import (TagListSerializerField,
                                TaggitSerializer)

from account.models import User
from account.api.serializers import UserLessInfoSerializer


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        exclude_fields = kwargs.pop("exclude_fields", None)
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)
        if exclude_fields is not None:
            for field_name in exclude_fields:
                self.fields.pop(field_name)


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="get_username")

    class Meta:
        model = User
        fields = ("username",)


class PageDetailSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField(default=[])

    class Meta:
        model = Page
        fields = [
            "id",
            "avatar",
            "cover",
            "name",
            "about",
            "description",
            "address",
            "location",
            "category",
            "directories",
            "projects",
            "books",
            "mobile",
            "email",
            "price",
            "hours",
            "tags",
            "day",
            "month",
            "year",
            "category",
            "page_type",
            "subscribers",
            "moderators",
            "creator",
            "created",
            "subscriber_count",
            "likes_count",
            "is_deleted",
            "slug",
            "numPosts",
            "online_count",
        ]
        depth = 1


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = "__all__"


class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = ("text",)


class RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = ("id", "page", "title", "text")


class LinkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Link
        fields = ("id", "page", "image", "title", "url")


class SocialSerializer(serializers.ModelSerializer):

    class Meta:
        model = Social
        fields = ("id", "page", "title", "url")

def voted(user, comment, value):
    return user.is_active and bool(user.vote_set.filter(comment=comment, value=value))


def voted_post(user, post, value):
    return user.is_active and bool(user.vote_set.filter(post=post, value=value))


class RecursiveField(serializers.Serializer):
    def to_representation(self, instance):
        serializer = self.parent.parent.__class__(instance, context=self.context)
        return serializer.data


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = "__all__"


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = "__all__"

class PageCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = [
            "id",
            "subscriber_count", 
            "online_count"           
        ]