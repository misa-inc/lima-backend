from rest_framework import serializers
from trivia.models import *

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


class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = ("text",)


def voted(user, comment, value):
    return user.is_active and bool(user.vote_set.filter(comment=comment, value=value))


def voted_status(user, status, value):
    return user.is_active and bool(user.vote_set.filter(status=status, value=value))


class RecursiveField(serializers.Serializer):
    def to_representation(self, instance):
        serializer = self.parent.parent.__class__(instance, context=self.context)
        return serializer.data


class CommentSerializer_detailed(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "id",
            "status",
            "author",
            "parent_comment",
            "perpective",
            "report",
            "saved",
            "created",
            "text",
            "is_deleted",
            "saved_count",
            "report_count",
            "share_count",
            "voters",
            "votes",
            "has_perspective",
            "saved_count",
            "report_count",
            "child_comments",
            "created_time_ago",
        ]
        depth = 1


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class TriviaSerializer_detailed(serializers.ModelSerializer):
    tags = TagListSerializerField(default=[])

    class Meta:
        model = Trivia
        fields = [
            "id",
            "attachment",
            "video",
            "created",
            "link",
            "tags",
            "page",
            "directory",
            "trivia_type",
            "perpective",
            "category",
            "parent",
            "author",
            "report",
            "saved",
            "share_count",
            "saved_count",
            "report_count",
            "is_deleted",
            "is_reviewed",
            "has_perspective",
            "voters",
            "votes",
            "comments",
            "slug",
            "created_time_ago",
        ]
        depth = 2


class TriviaCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trivia
        fields = [
            "id",
            "votes",
            "comments",
            "share_count",
        ]

  
class CommentCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "id",
            "votes", 
            "share_count"           
        ]


class TriviaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trivia
        fields = "__all__"


class AnonTriviaSerializer(serializers.ModelSerializer):
    author = UserLessInfoSerializer(read_only=True)

    class Meta:
        model = Trivia
        fields = ["id", "title", "author"]


class LessCommentSerializer(serializers.ModelSerializer):
    Trivia_id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "body", "trivia_id"]

    def get_trivia_id(self, obj):
        return obj.trivia.id
