from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from project.api.serializers import ProjectCountSerializer
from project.models import Project


def get_project_data(projectId):
    projects = Project.objects.filter(id__in=projectId)
    serializer = ProjectCountSerializer(projects, many=True)
    return serializer.data



class ProjectConsumer(WebsocketConsumer):

    def fetch_project(self, data):
        updates = get_project_data(data['projectId'])
        content = {
            'command': 'fetch_project',
            'update': updates
        }
        self.send_message(content)

    commands = {
        'fetch_project': fetch_project,
    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['project_id']
        self.room_project_name = 'project_%s' % self.room_name
        async_to_sync(self.channel_layer.project_add)(
            self.room_project_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.project_discard)(
            self.room_project_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_message(self, message):
        self.send(text_data=json.dumps(message))
