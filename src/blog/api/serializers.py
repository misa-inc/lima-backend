from rest_framework import serializers
from taggit.serializers import (TagListSerializerField,
                                TaggitSerializer)

from blog.models import Blog, Comment

# create serializers 


class BlogListSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField(method_name='get_author')
    category = serializers.SerializerMethodField(method_name='get_category')

    def get_author(self,obj):
        return {
            "first_name":obj.author.first_name,
            "last_name":obj.author.last_name,
        }

    def get_category(self,obj):
        category = [cat.title for cat in obj.category.get_queryset().only("title")]
        return category

    class Meta:
        model = Blog
        exclude = [
            'id', 'likes',
            'create', 'body', 
            'status', 'updated', 
            'publish', 'visits', 
            'special', 'category', 
            'directory', 'page' 
        ]


class BlogCreateSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField(default=[])

    class Meta:
        model = Blog
        fields = [
            'title', 'body',
            'image', 'summary',
            'category', 'publish',
            'special', 'status', 'tags',
            'directory', 'page' 
        ]


class BlogDetailUpdateDeleteSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField(method_name='get_author')
    slug = serializers.ReadOnlyField()

    def get_author(self,obj):
        return {
            "first_name":obj.author.first_name,
            "last_name":obj.author.last_name,
        }

    likes = serializers.SerializerMethodField(method_name='get_likes')

    def get_likes(self, obj):
        return obj.likes.count()

    class Meta:
        model = Blog
        exclude =[
            "create", "updated",
        ]
        read_only_fields = [
            "likes",
        ]


class CommentListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return {
            "name":obj.user.first_name,
        }


    class Meta:
        model = Comment
        fields = [
            "user", "name",
            "parent", "body",
            "create", "object_id",
            'likes'
        ]


class CommentUpdateCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "object_id", "name",
            "parent", "body",
            'likes'
        ]

