import json

import websockets


async def get_currency_rate_binance(pair: str = 'btcusdt'):
    binance_ws = f'wss://stream.binance.com:9443/stream?streams={pair}@miniTicker'

    async with websockets.connect(binance_ws) as client:
        data = json.loads(await client.recv())['data']
        print(data)
        return {'pair': data['s'], 'price': data['c']}