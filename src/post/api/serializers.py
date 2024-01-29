from rest_framework import serializers
from post.models import *

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


def voted_post(user, post, value):
    return user.is_active and bool(user.vote_set.filter(post=post, value=value))


class RecursiveField(serializers.Serializer):
    def to_representation(self, instance):
        serializer = self.parent.parent.__class__(instance, context=self.context)
        return serializer.data


class CommentSerializer_detailed(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "id",
            "post",
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


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"



class AnswerSerializer_detailed(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = [
            "id",
            "post",
            "author",
            "parent_snswer",
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
            "child_answers",
            "created_time_ago",
        ]
        depth = 1


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = "__all__"


class PostSerializer_detailed(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = [
            "id",
            "attachment",
            "video",
            "file",
            "created",
            "link",
            "text",
            "post_type",
            "is_walk_through",
            "perpective",
            "category",
            "parent",
            "author",
            "report",
            "saved",
            "page",
            "post_status",
            "directory",
            "share_count",
            "saved_count",
            "report_count",
            "is_deleted",
            "is_repost",
            "is_reviewed",
            "has_perspective",
            "voters",
            "votes",
            "reposts",
            "comments",
            "slug",
            "created_time_ago",
        ]
        depth = 2


class PostCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "id",
            "votes",
            "reposts",
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


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"


class AnonPostSerializer(serializers.ModelSerializer):
    author = UserLessInfoSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ["id", "title", "author"]


class LessCommentSerializer(serializers.ModelSerializer):
    post_id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "body", "post_id"]

    def get_post_id(self, obj):
        return obj.post.id
