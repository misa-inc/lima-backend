from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from directory.api.serializers import DirectoryCountSerializer
from directory.models import Directory


def get_directory_data(directoryId):
    directories = Directory.objects.filter(id__in=directoryId)
    serializer = DirectoryCountSerializer(directories, many=True)
    return serializer.data


class DirectoryConsumer(WebsocketConsumer):

    def fetch_directory(self, data):
        updates = get_directory_data(data['directoryId'])
        content = {
            'command': 'fetch_directory',
            'update': updates
        }
        self.send_message(content)

    commands = {
        'fetch_directory': fetch_directory,
    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['directory_id']
        self.room_directory_name = 'directory_%s' % self.room_name
        async_to_sync(self.channel_layer.directory_add)(
            self.room_directory_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.directory_discard)(
            self.room_directory_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_message(self, message):
        self.send(text_data=json.dumps(message))
