from channels.generic.websocket import AsyncJsonWebsocketConsumer
from communication.utils import ConsumerGroup
from communication.utils.message_types import MessageTypes
from channels.db import database_sync_to_async
from communication.models import Chatroom

#This consumers assumes the endpoint for creating chatrooms has already created the database record
class ChatroomConsumer(AsyncJsonWebsocketConsumer):
    is_private = False
    is_authenticated = False
    room_name = None
    room = None
    
    async def receive_json(self, content : dict, **kwargs):
        #If we're receiving a message and have already been authorized
        if(content['msg_type'] == MessageTypes.MESSAGE.value and self.is_authenticated):
            await self.channel_layer.group_send(
                self.room_name,
                {
                    "type": "receive.message.client",
                    "message": content["message"],
                    "channel_name": self.channel_name
                }
            )

        #If we're not already authenticated and the client attempts to send an authorization attempt
        elif (content['msg_type'] == MessageTypes.AUTHORIZATION_ATTEMPT.value and self.is_authenticated == False):
            password = content['password']
            result = await self.attempt_authorization(password)
            if(result):
                self.is_authenticated = True
                await self.send_authorization_successful()
            else:
                await self.send_authorize_request()
        print("received a message")

    async def send_json(self, content : object, **kwargs):
        await super().send_json(content)

    async def connect(self) -> None :
        
        #Get the room_name the user is attempting to connect to
        #Unfortunately, the default Javascript WS class doesn't allow custom headers
        #As a result, we have to sneek the room name in
        subprotocols = self.scope.get('subprotocols', [])
        if not subprotocols:
            await self.close()
            return
        self.room_name = subprotocols[0]
        await self.accept(subprotocol=self.room_name)
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        self.is_private = await self.check_if_private(channel_name=self.room_name)
        if(self.is_private):
            await self.send_authorize_request()
        else:
            self.is_authenticated = True
        print(self.room_name)
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
    async def disconnect_procedure(self) -> None:
        if self.room_name and self.room is not None:
            await self.channel_layer.group_discard(group=self.room_name, channel=self.channel_name)
            await database_sync_to_async(lambda: self.room.safely_decrement_count())()


    async def send_authorize_request(self) -> None:
        await database_sync_to_async(lambda: self.room.safely_increment_count())()
        await self.send_json({
            "msg_type": MessageTypes.AUTHORIZATION_REQUEST.value
        })

    async def send_authorization_successful(self) -> None:
        await self.send_json({
            "msg_type": MessageTypes.AUTHORIZATION_SUCCESS.value
        })
    async def attempt_authorization(self, password : str) -> bool:
        database_sync_to_async(lambda: self.room.refresh_from_db())()
        return self.room.is_password_valid(password=password)

    async def check_if_private(self, channel_name : str) -> bool:
        try:
            self.room = await database_sync_to_async(Chatroom.objects.get)(channel_name=channel_name)
            return self.room.is_private()
        except Chatroom.DoesNotExist:
            return False
