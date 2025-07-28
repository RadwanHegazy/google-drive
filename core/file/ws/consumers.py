from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json

class SessionConsumer (WebsocketConsumer) :

    def connect(self):
        self.user = self.scope['user']

        if not self.user.is_authenticated:
            self.close()
            return
        
        self.accept()
        # self.session_id = self.scope['url_route']['kwargs']['session_id']
        # async_to_sync(self.channel_layer.group_add)(
        #     self.GROUP,
        #     self.channel_name
        # )

    def disconnect(self, code):
        # async_to_sync(self.channel_layer.group_discard)(
        #     self.GROUP,
        #     self.channel_name
        # )
        pass

    def receive(self, text_data):
        print('recived : ', text_data)
    
    # def sendOrder (self, event):
        # data = json.dumps(event['event'])
        # self.send(text_data=data)
        # pass
