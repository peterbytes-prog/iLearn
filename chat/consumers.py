import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.utils import timezone
from datetime import datetime

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # accept connection
        self.id = self.scope.get('url_route', {}).get('kwargs', {}).get('course_id')
        self.user = self.scope.get('user')
        self.room_group_name = "chat_%s"%self.id
        #join room group
        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
        self.accept()
    def disconnect(self,  close_code):
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)
        pass
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        async_to_sync(self.channel_layer.group_send)(self.room_group_name, {
            'type':'chat_message',
            'message':message,
            'profile_photo':f"{self.user.student.photo.url}",
            'profile_link':f"{self.user.student.get_absolute_url()}",
            'user':self.user.username,
            'datetime':datetime.now().isoformat(),
        })
    def chat_message(self, event):
        self.send(text_data=json.dumps(event))
