import json
import logging
import asyncio
import worker_database.models
from uuid import UUID

import torch
from concurrent.futures import ThreadPoolExecutor
from aio_pika import connect_robust
from aio_pika.abc import AbstractIncomingMessage
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

from worker_config.config import settings
from worker_database.repository.message_repository import MessageRepository
from worker_database.repository.transaction_repository import TransactionRepository
from worker_service.service import Service

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MLWorker:
    def __init__(self):
        self._model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
        self._pipe = None
        self._executor = ThreadPoolExecutor(max_workers=1)
        self._channel = None
        self._service = Service(MessageRepository(), TransactionRepository())

    def _load_model(self):
        logger.info(f"Loading model {self._model_name}...")
        self._pipe = pipeline(
            "text-generation",
            model=self._model_name,
            torch_dtype=torch.float32,
            device_map="cpu"
        )
        logger.info("Model loaded successfully")

    def _predict(self, body: bytes) -> dict:
        data = body.decode('utf-8')
        messages = [
            {"role": "system", "content": "You are a friendly chatbot who always responds in the style of a pirate"},
            {"role": "user", "content": data},
        ]
        prompt = self._pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        outputs = self._pipe(prompt, max_new_tokens=128, do_sample=True, temperature=0.7, return_full_text=False)
        return {"prediction": outputs[0]["generated_text"]}

    async def _process_message(self, message: AbstractIncomingMessage):
        try:
            logger.info(f"Received request: {message.correlation_id}")
            message_id = message.correlation_id
            user_id = message.properties.headers['user_id']
            if not message_id or not user_id:
                raise ValueError("Please provide message_id and user_id")
            loop = asyncio.get_running_loop()
            result = await loop.run_in_executor(self._executor, self._predict, message.body)
            if result and 'prediction' in result:
                await self._service.process_success_result(UUID(message_id), json.dumps(result['prediction']))
            else:
                await self._service.process_unsuccess_result(UUID(message_id), UUID(user_id))
            await message.ack()
            logger.info(f"Processed response for {message.correlation_id}")
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            await message.reject(requeue=False)

    async def run(self):
        self._load_model()
        connection = await connect_robust(
            host="rabbitmq",
            port=5672,
            virtual_host='/',
            login=settings.RABBIT_MQ_USER,
            password=settings.RABBIT_MQ_PASSWORD,
            heartbeat=60
        )

        async with connection:
            self._channel = await connection.channel()
            await self._channel.set_qos(prefetch_count=1)
            queue = await self._channel.declare_queue("requests")
            logger.info("Worker is waiting for messages...")
            await queue.consume(self._process_message, no_ack=False)

            try:
                await asyncio.Future()
            except asyncio.CancelledError:
                logger.info("Worker stopped")

if __name__ == "__main__":
    worker = MLWorker()
    asyncio.run(worker.run())