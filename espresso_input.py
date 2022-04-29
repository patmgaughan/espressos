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
from sequence import *

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
        print("returned")
        producer_task.cancel()



async def receiver(websocket, buffer):
    print("ready to receive")
    async for message in websocket:
        if message == "gameover":
            counts = await websocket.recv()
            counts = counts.split(",")
            await websocket.send("gameover")
            closingSeq(counts[0], counts[1])
            break
        if message == "start":
            print("starting seq")
            openingSeq()
        else:
            print(message + f"\n{''.join(buffer)}", end="", flush=True)


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
                    elif key == keys.BACKSPACE:
                        buffer.pop(-1)
                        print("\b \b", end="", flush=True)
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

    thread = threading.Thread(target=between_callback, daemon=True)
    thread.start()

    while True:
        await asyncio.sleep(5)



if __name__ == "__main__":
    asyncio.run(client())
