from rest_framework import serializers
from page.models import *

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


class PageDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Page
        fields = [
            "id",
            "avatar",
            "cover",
            "name",
            "description",
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
        fields = ("id", "Page", "title", "text")


class LinkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Link
        fields = ("id", "Page", "image", "title", "url")


def voted(user, comment, value):
    return user.is_active and bool(user.vote_set.filter(comment=comment, value=value))


def voted_post(user, post, value):
    return user.is_active and bool(user.vote_set.filter(post=post, value=value))


class RecursiveField(serializers.Serializer):
    def to_representation(self, instance):
        serializer = self.parent.parent.__class__(instance, context=self.context)
        return serializer.data


class PageCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = [
            "id",
            "subscriber_count", 
            "online_count"           
        ]