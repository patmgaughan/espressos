#!/usr/bin/env python

import asyncio
import websockets
import aioconsole
from pprint import pprint


async def client_listener():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        await websocket.send("output")
        async for message in websocket:
            print(message)


if __name__ == "__main__":
    asyncio.run(client_listener())