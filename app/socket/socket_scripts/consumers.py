import json
import logging

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer

logger = logging.getLogger(__name__)


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "default"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        logger.debug(f"connect(): connection done;")
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    async def receive(self, text_data=None, bytes_data=None):
        # Receive message from WebSocket

        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "chat.message", "message": message},
        )

    @staticmethod
    async def send_ws_msg(position: str, value: int, status: int) -> None:
        # Send message to room group
        channel_layer = get_channel_layer()
        await channel_layer.group_send(
            "default",
            {
                "type": "chat.message",
                "position": position,
                "value": value,
                "status": status,
            },
        )
        # logger.debug(f"send_ws_msg(): done; {position = }, {value = }")

    async def chat_message(self, event: dict):
        # Send message to WebSocket
        await self.send(
            text_data=json.dumps(
                {
                    "position": event.get("position"),
                    "value": event.get("value"),
                    "status": event.get("status"),
                }
            )
        )
        # logger.debug(f"chat_message(): send done; {event = }")
