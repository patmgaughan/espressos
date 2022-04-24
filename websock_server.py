#!/usr/bin/env python

import asyncio
import argparse
import websockets
import threading
from pprint import pprint
from player_ops import CMND_TO_FUNC
from order_list import OrderList
from order_generator import order_generator


import kitchen
import cook





async def server(kitch, clients, start_pos,
                order_list, completed_orders, expired_orders,
                game_over, lock, websocket):

    type = await websocket.recv()
    print("received type")

    if type == "input":

        async with lock:
            player = cook.Cook(kitch, start_pos, start_pos, "player")
            start_pos += 1

        pprint(globals())

        for ws in clients:
            await ws.send(str(kitch))

        while True:
            resp = await websocket.recv()

            async with lock:

                if (resp.startswith("get_")):
                    arg1 = resp.replace('get_', '')
                    resp = "get_"

                func_name = CMND_TO_FUNC.get(resp)

                if not func_name:
                    await websocket.send("not a command")
                    continue

                print(f"<<< {func_name}")


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
            for ws in clients:
                await ws.send(stringGame(player, kitch, order_list, (completed_orders, expired_orders)))

    if type == "output":
        clients.append(websocket)
        for ws in clients:
            await ws.send(str(kitch))
        while True:
            await asyncio.sleep(1)


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

    kitch = kitchen.Kitchen()
    kitch.setUp()
    clients = []
    start_pos = 1
    order_list = OrderList()
    completed_orders = 0
    expired_orders = 0
    game_over = threading.Event()
    lock = asyncio.Lock()

    #FIXME: make int immutable
    fun = lambda ws: server(kitch, clients, start_pos, order_list, completed_orders,
                            expired_orders, game_over, lock, ws)

    #TODO: put this somewhere else so it doesnt run before people connect
    order_thread = threading.Thread(target=order_generator,
                                    args=("hard", order_list, game_over),
                                    daemon=True)
    order_thread.start()
    print("started order thread")

    async with websockets.serve(fun, args.i, args.p, ping_interval=None):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())