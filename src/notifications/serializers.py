from rest_framework import serializers
from .models import Notification
from account.api.serializers import ListUserSerializer
from blog.api.serializers import BlogDetailUpdateDeleteSerializer
from post.api.serializers import PostSerializer_detailed,CommentSerializer_detailed
from trivia.api.serializers import TriviaSerializer_detailed


class NotificationSerializer(serializers.ModelSerializer):

    from_user = ListUserSerializer()
    to_user = ListUserSerializer()
    noti_count = serializers.SerializerMethodField(read_only=True)
    post = PostSerializer_detailed(read_only=True)
    trivia = TriviaSerializer_detailed(read_only=True)
    comment = CommentSerializer_detailed(read_only=True)
    blog = BlogDetailUpdateDeleteSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = ['id','from_user','to_user','noti_count','post','comment','blog','trivia','notification_type','comments','user_has_seen','created_time_ago']
        depth = 7

    def get_noti_count(self,obj):
        count = self.context.get('noti_count')
        return count
