import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync, sync_to_async
from channels.db import database_sync_to_async
from channels.exceptions import StopConsumer

class FeedSocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.groupname = 'feed'
        # self.room_group_name = 'test'

        await self.channel_layer.group_add(
        # self.room_group_name,
        self.groupname,
        self.channel_name
        )

        # WS accept
        await self.accept()

        # Message to be sent on connection
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'You are now connected',
        }))

    async def disconnect(self, code):

        await self.channel_layer.group_discard(
            # self.room_group_name,
            self.groupname,
            self.channel_name
        )

        print('Disconnected')

        raise StopConsumer()

    async def receive(self, text_data):

        text_data_json = json.loads(text_data)

        await self.channel_layer.group_send(
        # self.room_group_name,
        self.groupname,
        {
            'type': 'send_data',
            'value': text_data_json
        }
        )

        # print('>>>>', text_data_json)

    async def send_data(self, event):
        jsonValue = event['value']
        await self.send(text_data = json.dumps(jsonValue))
