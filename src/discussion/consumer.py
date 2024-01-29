from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Chat , Discussion , Visitor
from account.models import User
from bots import BotHandler
from datetime import datetime

from asgiref.sync import sync_to_async
import json, html, pytz
from account.models import Record


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        self.discussion_code = self.scope["url_route"]["kwargs"]["discussion_code"]
        self.group_discussion_code = f'chat_{self.discussion_code}'
        self.sender = str(self.scope.get("user"))

        self.discussion_model = await self.get_discussion_model()
        self.bots = await self.active_bots()
        self.bothandler = BotHandler(self.bots, self.group_discussion_code)
        
        if self.sender != "AnonymousUser":
            self.user = await self.get_user()
        else:
            self.user = None

        await self.channel_layer.group_add(self.group_discussion_code, self.channel_name)
        
        await self.channel_layer.group_send(
            self.group_discussion_code, 
            {
                "type":"chat_message",
                "message":"Joined the discussion!",
                "sender":self.sender
            }
        )

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_send(
            self.group_discussion_code,
            {
                "type":"chat.message",
                "message":"Left the discussion",
                "sender":self.sender
            }
        )
        await self.channel_layer.group_discard(self.group_discussion_code, self.channel_name)
    
    async def receive(self, text_data=None, bytes_data=None):


        json_data = json.loads(text_data)
        
        message = json_data.get('message')
    
        saved = await self.save_message(message)
        if saved: 
            date_created = str(saved.created)
        else:
            date_created = str(datetime.now(tz=pytz.UTC))
        
        await self.channel_layer.group_send(
            self.group_discussion_code, 
            {
                "type":"chat.message",
                "message":message,
                "sender":self.sender,
                "date":date_created
            }
        )
        
        bot = await self.bothandler.get_response(message)

        if bot:
            bot_object, response = bot 
            user = await self.get_bot_user(bot_object)
            if response:
                saved = await self.save_message(response, user=user)
            await self.channel_layer.group_send(
                self.group_discussion_code,
                {
                    "type":"bot.response",
                    "message":str(response),
                    "sender":str(user),
                    "date":str(saved.created)
                }

            )
    
    async def bot_response(self, text_data):
        message = text_data.get("message")
        sender = text_data.get("sender")
        date = text_data.get('date')

        await self.send(text_data=json.dumps({"message":message, "sender":sender, "date":date}))

    async def chat_message(self, text_data):
        
        is_blocked = await self.get_blocked()
        if is_blocked:
            return 0
        
        message = html.escape(text_data.get("message"))
        sender = text_data.get('sender')
        date = text_data.get('date')

        await self.send(text_data=json.dumps({"message":message,"sender":sender, 'date':date}))

    @database_sync_to_async
    def save_message(self, text: str, first_chat: str, file, user=None):
        if not user:
            user = self.user 
        
        if user:
            if first_chat == "1":
                chat = Chat.objects.create(
                    from_user=user,
                    text=text,
                    file=file,
                    first_chat=True
                )
            else:
                chat = Chat.objects.create(
                    from_user=user,
                    text=text,
                    file=file
                )    
            Record.objects.get_or_create(
                user=user,
                aura="6",
                discussions=self.discussion_model,
                time="3",
                type="minor",
                status="closed",
                description=(f"You earned 6 aura by engaging in this discussion “{self.discussion_model.discussion_name[:7]}...”")
            )
            user.total_aura = user.total_aura + 6
            user.save()
            
            self.discussion_model.chat_set.add(chat)

            return chat
    
    @database_sync_to_async 
    def get_discussion_model(self):
        return Discussion.objects.get(discussion_code=self.discussion_code)

    @database_sync_to_async
    def get_user(self):
        return User.objects.get(username=self.sender)
    
    @database_sync_to_async
    def get_blocked(self):
        if self.user and self.discussion_model:
            query = self.discussion_model.blocked_users.filter(username=self.user)
            return any(query)
    
    @database_sync_to_async
    def active_bots(self):
        bots = [x for x in self.discussion_model.active_bots.all()]
        return bots 
    
    @sync_to_async
    def bot_handler(self):
        return BotHandler(self.bots, self.group_discussion_code)
    
    @database_sync_to_async
    def get_bot_user(self, bot):
        return bot.user 
    
class NotifConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('notif_chat', self.channel_name)
    
        await self.accept()
    
    async def receive(self, text_data=None, bytes_data=None):
        data_json = json.loads(text_data)
        
        ip_addr = data_json.get('ip_address')
        user_agent = data_json.get('user_agent')

        if all([ip_addr, user_agent]):

            await self.save_visitor(ip_addr=ip_addr, user_agent=user_agent)
        
        total_visitor = await self.total_visitor()

        await self.channel_layer.group_send(
            'notif_chat',
            {
                'type':'send.notif',
                'total_visitor':total_visitor
            }
        )
    
    async def send_notif(self, text_data):

        await self.send(text_data=json.dumps(text_data))
    
    @database_sync_to_async
    def total_visitor(self):
        return Visitor.objects.all().count()
    
    @database_sync_to_async
    def save_visitor(self, ip_addr, user_agent):
        if Visitor.objects.filter(ip_addr=ip_addr).first():
            return None
        v = Visitor(ip_addr=ip_addr, user_agent=user_agent)
        v.save()
        return v