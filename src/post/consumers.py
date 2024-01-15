from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from post.api.serializers import PostCountSerializer, CommentCountSerializer
from post.models import Post, Comment


def get_posts_data(postId):
    posts = Post.objects.filter(id__in=postId)
    serializer = PostCountSerializer(posts, many=True)
    return serializer.data

def get_comments_data(commentId):
    comments = Comment.objects.filter(id__in=commentId)
    serializer = CommentCountSerializer(comments, many=True)
    return serializer.data


class TimelineConsumer(WebsocketConsumer):

    def fetch_post(self, data):
        updates = get_posts_data(data['postsId'])
        if updates:
            content = {
                'command': 'fetch_post',
                'update': updates
            }
            self.send_message(content)

    def fetch_comment(self, data):
        updates = get_comments_data(data['commentsId'])
        if updates:
            content = {
                'command': 'fetch_comment',
                'update': updates
            }
            self.send_message(content)        

    commands = {
        'fetch_post': fetch_post,
        'fetch_comment': fetch_comment,
    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['user_id']
        self.room_group_name = 'timeline_%s' % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)      
        self.commands[data['command']](self, data)

    def send_message(self, message):
        self.send(text_data=json.dumps(message))
