from rest_framework import serializers
from directory.models import *

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


class DirectoryDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Directory
        fields = [
            "id",
            "avatar",
            "cover",
            "name",
            "about",
            "description",
            "code_of_conduct",
            "day",
            "month",
            "year",
            "category",
            "pages",
            "projects",
            "books",
            "directory_type",
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


class DirectorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Directory
        fields = "__all__"


class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = ("text",)


class RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = ("id", "directory", "title", "text")


class LinkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Link
        fields = ("id", "directory", "image", "title", "url")


class RecursiveField(serializers.Serializer):
    def to_representation(self, instance):
        serializer = self.parent.parent.__class__(instance, context=self.context)
        return serializer.data


class DirectoryCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Directory
        fields = [
            "id",
            "subscriber_count", 
            "online_count"           
        ]