#!/usr/bin/env python

import asyncio
import websockets
import aioconsole
from pprint import pprint


async def client_listener():
    parser = argparse.ArgumentParser(
        description='Performs some useful work.',
    )
    parser.add_argument(
        '-i',
        type=str,
        default='localhost',
        help='ip to run server on',
    )
    parser.add_argument(
        '-p',
        type=str,
        default='8765',
        help='port to run server on',
    )

    args = parser.parse_args()

    uri = f"ws://{args.i}:{args.p}"
    async with websockets.connect(uri) as websocket:
        await websocket.send("output")
        async for message in websocket:
            print(message)


if __name__ == "__main__":
    asyncio.run(client_listener())