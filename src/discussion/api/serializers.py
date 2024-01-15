from rest_framework import serializers
from discussion.models import Discussion, Chat, Bot


class DiscussionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discussion 
        fields = "__all__"
    

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat 
        fields = '__all__'
    

class BotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bot 
        fields = '__all__'