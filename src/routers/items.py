import logging

from fastapi import Query, HTTPException, APIRouter

from src.utils.fetch_currency import get_currency_rate_binance

router = APIRouter()
logger = logging.getLogger()


@router.get('/courses')
async def get_currency_courses(pair: str = 'btcusdt', exchanger: str = 'binance'):
    try:
        result = await get_currency_rate_binance(pair)
        return result
    except Exception as e:
        logger.error(f'An error occurred: {e}')