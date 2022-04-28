#!/usr/bin/env python

import asyncio
import argparse
import websockets
import aioconsole
import os
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

        await websocket.send(input("username: "))
        os.system("stty -echo")

        try:
            buffer = ""
            while True:
                key = getkey()

                if key == keys.UP:
                    print("up")
                    await websocket.send("w")
                    time.sleep(.3)
                elif key == keys.DOWN:
                    print("down")
                    await websocket.send("s")
                    time.sleep(.3)
                elif key == keys.LEFT:
                    print("left")
                    await websocket.send("a")
                    time.sleep(.3)
                elif key == keys.RIGHT:
                    print("right")
                    await websocket.send("d")
                    time.sleep(.3)

                else:  # Handle text characters
                    if key == "\n":
                        await websocket.send(buffer)
                        print(f"\n{buffer}")
                        buffer = ""
                    else:
                        print(key, end="", flush=True)
                        buffer += key

        except EOFError:
            pass
        except websockets.exceptions.ConnectionClosedError:
            print("hit error")
        finally:
            os.system("stty echo")

if __name__ == "__main__":
    asyncio.run(client())
