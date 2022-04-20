#!/usr/bin/env python

import asyncio
import websockets
import threading
from pprint import pprint
from player_ops import CMND_TO_FUNC
from order_list import OrderList
from order_generator import order_generator


import kitchen
import cook


kitch = kitchen.Kitchen()
kitch.setUp()

output_clients = []

start_pos = 1
order_list = OrderList()
completed_orders = 0
expired_orders = 0
game_over = threading.Event()

async def output(websocket):
    global output_clients
    output_clients.append(websocket)
    while True:
        pass

async def input(websocket):
    global kitch
    global clients
    global start_pos
    global order_list
    global completed_orders
    global expired_orders
    global game_over

    player = cook.Cook(kitch, start_pos, start_pos, "player")
    start_pos += 1

    pprint(globals())
    for ws in output_clients:
        await ws.send(str(kitch))
    print("clienst: ", clients)
    while True:
        resp = await websocket.recv()

        if (resp.startswith("get_")):
            arg1 = resp.replace('get_', '')
            resp = "get_"


        func_name = CMND_TO_FUNC.get(resp)

        if not func_name:
            await websocket.send("not a command")
            continue


        print(f"<<< {func_name}")

        # func = getattr(globals()["ops"], func_name)

        func = getattr(player, func_name)

        if resp == "serve":
            succ, msg = func()
            if succ:
                pizza = player.emptyHands()
                succ, msg = order_list.fulfillOrder(pizza)
                if succ:
                    completed_orders += 1
                else:
                    player.give(pizza)
        elif (resp == "get_"):
                succ, msg = func(arg1)
        else:
            func()

        expired_orders += order_list.removeExpired()

        print(stringGame(player, kitch, order_list, (completed_orders, expired_orders)))
        for ws in output_clients:
            await ws.send(stringGame(player, kitch, order_list, (completed_orders, expired_orders)))


def stringGame(player, kitchen, order_list, order_counts):
    board = [""] * (kitchen.HEIGHT + 1)

    board[0] = player.inventory()

    for i in range(kitchen.HEIGHT):
        board[i + 1] = kitchen.getRow(i)

    board[1] += "      Order Queue" + "      Completed Orders: \033[32m{}".format(order_counts[0])
    board[2] += " ---------------------" + " Expired Orders:   \033[91m{}".format(order_counts[1])

    topFive = order_list.topFive()
    for i in range(len(topFive)):
        board[i + 3] += " {}) {}".format(i + 1, topFive[i])

    return "\n".join(board)


async def main():
    #TODO: put this somewhere else
    order_thread = threading.Thread(target=order_generator,
                                    args=("hard", order_list, game_over),
                                    daemon=True)
    order_thread.start()
    print("started order thread")

    async with websockets.serve(input, "10.247.83.240", 8765):
        await asyncio.Future()  # run forever


    async with websockets.serve(output, "10.247.83.240", 8764):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())