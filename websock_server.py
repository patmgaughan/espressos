#!/usr/bin/env python

import asyncio
import websockets
from pprint import pprint

import kitchen
import cook
import oven
import counter


kitch = kitchen.Kitchen()
player1 = cook.Cook(kitch, 3, 3, "player1")
player2 = cook.Cook(kitch, 4, 4, "player2")
oven.Oven(kitch, 6, 6)
oven.Oven(kitch, 6, 5)
counter.Counter(kitch, 2, 0)
counter.Counter(kitch, 3, 0)
kitch.print()

clients = []


async def hello(websocket):
    global kitch
    global clients
    global player1
    pprint(globals())
    clients.append(websocket)
    print("clienst: ", clients)
    while True:
        resp = await websocket.recv()
        meth, func_name = resp.split()
        print(f"<<< {func_name}")

        # func = getattr(globals()["ops"], func_name)

        func = getattr(globals()[meth], func_name)
        func()

        kitch.print()
        for ws in clients:
            await ws.send(str(kitch))



async def main():
    async with websockets.serve(hello, "localhost", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())