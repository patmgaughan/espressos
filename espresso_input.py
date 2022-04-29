#!/usr/bin/env python

import asyncio
import argparse
import websockets
import aioconsole
import threading
import os
import sys
import select
from getkey import getkey, keys
import time

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
        buffer = []
        producer_wrapper = lambda ws: producer(ws, buffer)
        receiver_wrapper = lambda ws: receiver(ws, buffer)

        consumer_task = asyncio.ensure_future(
            receiver_wrapper(websocket))
        print("consuming")
        producer_task = asyncio.ensure_future(
            producer_wrapper(websocket))
        print("producing")
        done, pending = await asyncio.wait(
            [consumer_task, producer_task],
            return_when=asyncio.FIRST_COMPLETED,
        )


async def receiver(websocket, buffer):
    print("ready to receive")
    async for message in websocket:
        print(message + f"\n{''.join(buffer)}", end="", flush=True)

async def async_getkey():
  while True:
    await asyncio.sleep(0.1)
    print("waiting t or")
    while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        ch = sys.stdin.read(1)
        print('none block input char', ch)

async def producer(websocket, buffer):
    async def do():
        await websocket.send(input("username: "))
        os.system("stty -echo")
        print("here")
        try:
            while True:

                key = getkey()

                if key == keys.UP:
                    await websocket.send("w")
                    await asyncio.sleep(.3)
                elif key == keys.DOWN:
                    await websocket.send("s")
                    await asyncio.sleep(.3)
                elif key == keys.LEFT:
                    await websocket.send("a")
                    await asyncio.sleep(.3)
                elif key == keys.RIGHT:
                    await websocket.send("d")
                    await asyncio.sleep(.3)

                else:  # Handle text characters
                    if key == "\n":
                        temp = [c for c in buffer]
                        buffer.clear()
                        await websocket.send(temp)
                        print(f"\n{''.join(temp)}", flush=True, end="")
                    else:
                        print(key, end="", flush=True)
                        buffer.append(key)
        except EOFError:
            pass
        except websockets.exceptions.ConnectionClosedError:
            print("hit error")
        finally:
            os.system("stty echo")

    def between_callback():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        loop.run_until_complete(do())
        loop.close()

    thread = threading.Thread(target=between_callback)
    thread.start()

    while True:
        await asyncio.sleep(5)



if __name__ == "__main__":
    asyncio.run(client())
