from uuid import UUID

import pika
from pika.adapters.blocking_connection import BlockingConnection

from configuration.rabbit_conn import REQUESTS_QUEUE_NAME
from database.repository.message_repository import MessageRepository
from model.message_status import MessageStatus

from model.message_type import MessageType

class MLService:
    def __init__(self,
                 message_repository: MessageRepository,
                 connection: BlockingConnection,
                 ):
        self._message_repository = message_repository
        self._connection = connection
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=REQUESTS_QUEUE_NAME)


    def predict(self, input_data: str, chat_id: UUID, user_id: UUID) -> str:
        self._message_repository.add_message_to_chat(chat_id, input_data, MessageType.USER, MessageStatus.PROCESSED)
        resp_message = self._message_repository.add_message_to_chat(chat_id, "", MessageType.SYSTEM, MessageStatus.PROCESSING)
        request_id = str(resp_message.id)
        headers = {
            "user_id": str(user_id)
        }
        self._channel.basic_publish(
            exchange="",
            routing_key=REQUESTS_QUEUE_NAME,
            properties=pika.BasicProperties(
                correlation_id= request_id,
                headers=headers,
            ),
            body=input_data
        )
        return request_id

    def get_answer(self, message_id: UUID, user_id: UUID):
        return self._message_repository.get_message(message_id, user_id)



