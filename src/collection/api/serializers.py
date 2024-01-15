from rest_framework import serializers
from collection.models import *

from account.models import User


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


class CollectionDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Collection
        fields = [
            "id",
            "name",
            "description",
            "day",
            "month",
            "year",
            "collection_type",
            "posts",
            "trivias",
            "competitions",
            "events",
            "articles",
            "books",
            "directories",
            "discussions",
            "creator",
            "created",
            "share_count",
            "is_deleted",
            "slug",
        ]
        depth = 1


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = "__all__"


class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = ("text",)


class RecursiveField(serializers.Serializer):
    def to_representation(self, instance):
        serializer = self.parent.parent.__class__(instance, context=self.context)
        return serializer.data
