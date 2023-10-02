from channels.generic.websocket import AsyncWebsocketConsumer
from user_profile.models import UserProfile 
from channels.db import database_sync_to_async
from .models import ChatModel

import json


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.receiver_id = self.scope['url_route']['kwargs']['receiver_id']
        self.user = self.scope['user']
        self.rprofile = await  database_sync_to_async(
            UserProfile.objects.get)(id=int(self.receiver_id))
        
        self.sprofile = await database_sync_to_async(UserProfile.objects.get)(
            user=self.user
        )
        self.chat_limit = [
            f'chat_{self.sprofile.name}-{self.rprofile.name}',
            f'chat_{self.rprofile.name}-{self.sprofile.name}'
        ]
        self.room_group_name = f'chat_{self.sprofile.name}-{self.rprofile.name}'
        print(self.room_group_name)
        print(self.chat_limit)
        if self.room_group_name in self.chat_limit:
            print("is happening")
            #self.room_group_name = ''.join(sorted(self.room_group_name))
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
    async def receive(self,text_data):
        print('inreceive')
        print(text_data)
        text_json_data = json.loads(text_data)
        message = text_json_data['message']
        print(message)
        self.sender = await database_sync_to_async(UserProfile.objects.get)(
            id=text_json_data['sender']
        )
        self.receiver = await database_sync_to_async(UserProfile.objects.get)(
            id=text_json_data['receiver']
        )
        await database_sync_to_async(ChatModel.objects.create)(
            sender=self.sender, receiver=self.receiver, message=message 
        )
        if self.room_group_name == self.chat_limit[0]:
            send_to = self.chat_limit[1]
        elif self.room_group_name == self.chat_limit[1]:
            send_to = self.chat_limit[0]
        await self.channel_layer.group_send(
            send_to,
            {
                "type":"chat_message",
                "message": message
            }
        )
    async def chat_message(self,event):
        message = event['message']
        print('chat',message)
        await self.send(
            text_data=json.dumps(
                {'message': message,'sender':self.sprofile.name}
            )
        )
    async def disconnect(self,close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
        
        