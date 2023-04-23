import json
import asyncio

from websockets import connect

from settings import settings
from core import uniswap_parser

async def main():
    print("Listening for new blocks...")

    async with connect(settings.INFURA_WS_URL, ping_interval=2) as websocket:
        await websocket.send(json.dumps({
            "id": 1,
            "method": "eth_subscribe",
            "params": ["newHeads"]
        }))

        while True:
            message = await websocket.recv()
            message = json.loads(message)

            if 'params' in message:
                new_block = message['params']['result']

                block_number = int(new_block['number'], 16)
                print(f"New block detected: {block_number}")

                uniswap_parser.print_swap_events_for_block(block_number)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
