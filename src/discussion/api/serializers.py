from rest_framework import serializers
from discussion.models import Discussion, Chat, Bot, Category
from taggit.serializers import (TagListSerializerField,
                                TaggitSerializer)

class DiscussionSerializer(serializers.ModelSerializer):
    labels = TagListSerializerField(default=[])

    class Meta:
        model = Discussion 
        fields = "__all__"
    

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat 
        fields = ['discussion','file','from_user','text','created','liked_users','day','month','year','time','created_time_ago']


class BotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bot 
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category 
        fields = '__all__'        