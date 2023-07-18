from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': "tester_message", # nombre de la funcion
                'tester': f'Bienvenido al chat {self.room_group_name}'     
            }
        )

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)

        if text_data_json.get('chat_message'):
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': "chat_message", # nombre de la funcion
                    'chat_messages': text_data_json['chat_message']   
                }
            )
        else:
            print(text_data_json.get('message', ''))
    
    async def tester_message(self, event):        
        tester = event['tester']
        await self.send(text_data=json.dumps({"tester":tester,}))
        
        
    async def chat_message(self, event):
        messsage = event['chat_messages']
        await self.send(text_data=json.dumps({"messsage":messsage,}))
            

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name    
        )