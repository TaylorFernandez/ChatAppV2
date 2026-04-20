from channels.generic.websocket import AsyncJsonWebsocketConsumer
from communication.utils import ConsumerGroup

class GlobalChatConsumer(AsyncJsonWebsocketConsumer):
    async def receive_json(self, content : dict, **kwargs):
        await self.channel_layer.group_send(
            ConsumerGroup.GLOBAL.value,
            {
                "type": "receive.message.client",
                "message": content["message"],
                "channel_name": self.channel_name
            }

        )
        print("received a message")

    async def send_json(self, content : object, **kwargs):
        await super().send_json(content)

    async def connect(self) -> None :
        await self.channel_layer.group_add(group=ConsumerGroup.GLOBAL.value, channel=self.channel_name)
        await self.accept()
        print(f"Client connected to group {ConsumerGroup.GLOBAL.value}")

    async def disconnect(self, close_code):
        await self.disconnect_procedure()

    async def close(self, subprotocol=None):
        await self.disconnect_procedure()
    
    async def receive_message_client(self, event):
        if event["channel_name"] != self.channel_name:
            await self.send_json(
                {
                    "message": event["message"],
                    "channel_name": event["channel_name"]
                }
            )

   #since most of the disconnect procedure will be the same when the client gets disconnected or closes the connection
   #Most of the disconnect procedure can be abstracted into a method that gets called both event handlers
    async def disconnect_procedure(self):
        await self.channel_layer.group_discard(group=ConsumerGroup.GLOBAL.value, channel=self.channel_name)