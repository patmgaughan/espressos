"""
  client.py
  Description: A module containing distributed espresso's express client code

  Authors: Jackson Clayton
"""
#!/usr/bin/env python

import asyncio
import argparse
import websockets
import threading
import os
import sys
from getkey import getkey, keys
import time
from sequence import *


async def client():
    """
    parse command line arguments, then connect to server websocket
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--ip', '-i',
        type=str,
        default='localhost',
        help='ip to connect to server on',
    )
    parser.add_argument(
        '--port', '-p',
        type=str,
        default='8765',
        help='port to connect to server on',
    )

    args = parser.parse_args()

    uri = f"ws://{args.ip}:{args.port}"

    async with websockets.connect(uri, ping_interval=None) as websocket:
        #await websocket.send("input")
        buffer = []

        async def producer_wrapper(ws):
            await message_producer(ws, buffer)

        async def receiver_wrapper(ws):
            await message_receiver(ws, buffer)

        # run producer and consumer until one returns
        consumer_task = asyncio.ensure_future(
            receiver_wrapper(websocket))
        producer_task = asyncio.ensure_future(
            producer_wrapper(websocket))
        await asyncio.wait(
            [consumer_task, producer_task],
            return_when=asyncio.FIRST_COMPLETED)

        # cancel outstanding producer task
        producer_task.cancel()


async def message_receiver(websocket, buffer):
    """
    asynchronous function for receiving game state from server and playing
    start and stop animations
    """
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
            print(f"\n{message}\n{''.join(buffer)}", end="", flush=True)


async def message_producer(websocket, buffer):
    """
    asynchronous function for receiving input from the keyboard and sending it
    to the server as commands
    this function runs get_input as a coroutine to allow for asynchronous
    keypress detection
    """
    async def get_input():
        """
        continuously detect keypresses until killed
        """
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
                    if key == keys.ENTER:
                        temp = [c for c in buffer]
                        buffer.clear()
                        await websocket.send(temp)
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
        """
        callback function to schedule get_input in separate thread
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        loop.run_until_complete(get_input())
        loop.close()

    # run between_callback in new thread
    thread = threading.Thread(target=between_callback, daemon=True)
    thread.start()

    # run until killed
    while True:
        await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(client())
