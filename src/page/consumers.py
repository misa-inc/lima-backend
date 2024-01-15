from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from page.api.serializers import PageCountSerializer
from page.models import Page


def get_page_data(pageId):
    pages = Page.objects.filter(id__in=pageId)
    serializer = PageCountSerializer(pages, many=True)
    return serializer.data



class PageConsumer(WebsocketConsumer):

    def fetch_page(self, data):
        updates = get_page_data(data['pageId'])
        content = {
            'command': 'fetch_page',
            'update': updates
        }
        self.send_message(content)

    commands = {
        'fetch_page': fetch_page,
    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['page_id']
        self.room_page_name = 'page_%s' % self.room_name
        async_to_sync(self.channel_layer.page_add)(
            self.room_page_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.page_discard)(
            self.room_page_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_message(self, message):
        self.send(text_data=json.dumps(message))
