import logging

from fastapi import APIRouter
import aio_pika

from src.utils.fetch_currency import get_currency_rate_binance

router = APIRouter()
logger = logging.getLogger(__name__)

RABBITMQ_CONNECTION_STRING = "amqp://guest:guest@localhost/"
ERROR_QUEUE_NAME = "error_queue"


async def create_rabbitmq_connection():
    return await aio_pika.connect_robust(RABBITMQ_CONNECTION_STRING)


async def publish_error_message(message):
    connection = await create_rabbitmq_connection()
    async with connection:
        channel = await connection.channel()
        error_queue = await channel.declare_queue(ERROR_QUEUE_NAME)
        await channel.default_exchange.publish(
            aio_pika.Message(body=message.encode()),
            routing_key=error_queue.name,
        )


@router.get('/courses')
async def get_currency_courses(pair: str = 'btcusdt', exchanger: str = 'binance'):
    try:
        result = await get_currency_rate_binance(pair)
        return result
    except Exception as e:
        logger.error(f"An error occurred: {e}")

        await publish_error_message(f"An error occurred: {e}")

        return {"error": "An error occurred"}
