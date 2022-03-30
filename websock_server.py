#!/usr/bin/env python

import asyncio
import websockets
from pprint import pprint

import kitchen
import cook
import oven
import counter


kitch = kitchen.Kitchen()
oven.Oven(kitch, 6, 6)
oven.Oven(kitch, 6, 5)
counter.Counter(kitch, 2, 0)
counter.Counter(kitch, 3, 0)
kitch.print()

clients = []

start_pos = 1

async def hello(websocket):
    global kitch
    global clients
    global start_pos
    player = cook.Cook(kitch, start_pos, start_pos, "player")
    start_pos += 1

    pprint(globals())
    clients.append(websocket)
    for ws in clients:
        await ws.send(str(kitch))
    print("clienst: ", clients)
    while True:
        resp = await websocket.recv()
        func_name = resp.strip()
        print(f"<<< {func_name}")

        # func = getattr(globals()["ops"], func_name)

        func = getattr(player, func_name)
        func()

        kitch.print()
        for ws in clients:
            await ws.send(str(kitch))



async def main():
    async with websockets.serve(hello, "localhost", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())