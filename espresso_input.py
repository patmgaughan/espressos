#!/usr/bin/env python

import asyncio
import argparse
import websockets
import aioconsole
from pprint import pprint

async def client():
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
    async with websockets.connect(uri, ping_interval=None) as websocket:
        await websocket.send("input")
        try:
            while True:
                cmnd = input()
                await websocket.send(cmnd)
        except EOFError:
            pass

if __name__ == "__main__":
    asyncio.run(client())