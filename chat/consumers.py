from channels.generic.websocket import AsyncWebsocketConsumer
from user_profile.models import UserProfile 
from channels.db import database_sync_to_async
from .models import ChatModel, LiveChatModel 
from asgiref.sync import sync_to_async

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
        data = {
            'receiver_id':self.receiver.id,'sender_id':self.sender.id,
            'message':message,'type':'chat_message',
        }
        await self.channel_layer.group_send(
            "livechat_%s" % self.sender.name,
            data
        )
        await self.channel_layer.group_send(
            "livechat_%s" % self.receiver.name,
            data
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
        
        
class LiveChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'livechat_%s' % self.room_name
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
    async def disconnect(self,close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    async def chat_message(self,event):
        sender = await database_sync_to_async(
            UserProfile.objects.get)(id=event['sender_id'])
        receiver = await database_sync_to_async(
            UserProfile.objects.get)(id=event['receiver_id'])
        msg = event['message']
        sexist_queryset = await database_sync_to_async(LiveChatModel.objects.filter)(sender=sender,receiver=receiver)
        sexist = await database_sync_to_async(sexist_queryset.exists)()
        print(sexist)
        rexist_queryset = await database_sync_to_async(LiveChatModel.objects.filter)(sender=receiver,receiver=sender)
        rexist = await database_sync_to_async(rexist_queryset.exists)()
        print(rexist)
        if sexist or rexist:
            if sexist:
                objquery = await database_sync_to_async(LiveChatModel.objects.filter)(sender=sender,receiver=receiver)
            elif rexist:
                objquery = await database_sync_to_async(LiveChatModel.objects.filter)(
                    sender=receiver,receiver=sender)
            await database_sync_to_async(
                objquery.update)(sender=sender,message=msg,receiver=receiver)
        else:
            await database_sync_to_async(LiveChatModel.objects.create)(
                sender=sender,message=msg,receiver=receiver)
        obj = await database_sync_to_async(LiveChatModel.objects.get)(sender=sender,receiver=receiver)
        simg = await sync_to_async(lambda:obj.sender)()
        img = await sync_to_async(lambda:simg)()
        img_url = img.image.url
        msender = await sync_to_async(lambda:obj.sender)()
        sender_id = await sync_to_async(lambda:msender)()
        data = {
            'type':'chat_message',
            'img_url':img_url,
            'name':obj.sender.name,
            'obj_id':obj.id,
            'sender_id':sender_id.id,
            'message':msg,
        }
        await self.send(text_data=json.dumps(data))
        '''
        await self.channel_layer.group_send(
            self.room_group_name,
            data
        )
        '''
    '''
    async def chat_message(self,event):
        print(event)
        data = {
            'img_url':event['img_url'],
            'name':event['name'],
            'obj_id':event['obj_id'],
            'message':event['message'],
        }
        await self.send(text_data=json.dumps(data))'''

        
        