#!/usr/bin/env python

import asyncio
import websockets
import aioconsole
from pprint import pprint

async def receiver(websocket):
    print("ready to receive")
    async for message in websocket:
        print(message)

async def sender(websocket):
    try:
        while True:
            cmnd = await aioconsole.ainput()
            await websocket.send(cmnd)
    except EOFError:
        pass



async def hello():
    uri = "ws://10.247.83.240:8765"
    async with websockets.connect(uri) as websocket:
        consumer_task = asyncio.ensure_future(
            receiver(websocket))
        print("consuming")
        producer_task = asyncio.ensure_future(
            sender(websocket))
        print("producing")
        done, pending = await asyncio.wait(
            [consumer_task, producer_task],
            return_when=asyncio.FIRST_COMPLETED,
        )

if __name__ == "__main__":
    asyncio.run(hello())