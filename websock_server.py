#!/usr/bin/env python

import asyncio
import argparse
import websockets
import threading
import time
from pprint import pprint
from player_ops import CMND_TO_FUNC
from order_list import OrderList
from order_generator import order_generator
from order import Order
from threadsafe_counter import ThreadsafeCounter


import kitchen
import cook





async def server(kitch, clients, start_pos,
                order_list, completed_orders, expired_orders,
                game_over, lock, websocket):

    type = await websocket.recv()
    print("received type")

    if type == "input":

        # TODO: add option to give username

        async with lock:
            pos = start_pos.increment()
            player = cook.Cook(kitch, pos, pos, "player")

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
                            completed_orders.increment()
                        else:
                            player.give(pizza)
                elif (resp == "get_"):
                    succ, msg = func(arg1)
                else:
                    func()


                print(stringGame(player, kitch, order_list, (completed_orders, expired_orders)))
            for ws in clients:
                await ws.send(stringGame(player, kitch, order_list, (completed_orders, expired_orders)))

    if type == "output":
        clients.append(websocket)
        for ws in clients:
            await ws.send(str(kitch))
        while True:
            await asyncio.sleep(1)

    if type == "reprint":
        while True:
            await asyncio.sleep(5)
            for ws in clients:
                await ws.send(stringGame(player, kitch, order_list, (completed_orders, expired_orders)))

def stringGame(player, kitchen, order_list, order_counts):
    board = [""] * (kitchen.HEIGHT + 1)

    board[0] = player.inventory() if player is not None else ""

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
    start_pos = ThreadsafeCounter()
    order_list = OrderList()
    completed_orders = ThreadsafeCounter()
    expired_orders = ThreadsafeCounter()
    game_over = threading.Event()
    lock = asyncio.Lock()

    #FIXME: make int immutable
    fun = lambda ws: server(kitch, clients, start_pos, order_list, completed_orders,
                            expired_orders, game_over, lock, ws)

    print("started order thread")

    async def run_server():
        print("running server")
        async with websockets.serve(fun, args.i, args.p, ping_interval=None):
            await asyncio.Future()  # run forever

    async def run_orders(clients, expired_orders):
        print("running orders")

        # choose_difficulty(difficulty)
        # Returns:  order rate, the decay rate, and the rate cap
        # Purpose:  Return the difficulty settings for order generation
        def choose_difficulty(difficulty):
            if difficulty == "hard":
                order_rate = 30
                decay_rate = 0.9
                rate_cap = 5


            elif difficulty == "medium":
                order_rate = 45
                decay_rate = 0.94
                rate_cap = 10

            # make easy the fall-through case
            else:
                order_rate = 45
                decay_rate = 0.97
                rate_cap = 15

            return order_rate, decay_rate, rate_cap

        while True:
            order_rate, decay_rate, rate_cap = choose_difficulty("hard")

            # need start time so build_pizza can create more complex pizzas as
            # game progresses
            start_time = time.time()

            while True:
                pizza = Order.build_pizza(start_time)
                order = Order(pizza)
                order_list.add(order)

                # make sure the order_rate does not go below the rate cap
                order_rate = order_rate * decay_rate
                if order_rate < rate_cap:
                    order_rate = rate_cap

                expired_orders.add(order_list.removeExpired())

                print(stringGame(None, kitch, order_list, (completed_orders, expired_orders)))

                for ws in clients:
                    await ws.send(stringGame(None, kitch, order_list, (completed_orders, expired_orders)))
                await asyncio.sleep(order_rate)


    # task1 = asyncio.create_task()
    # task2 = asyncio.create_task()
    print("tasks created")
    await asyncio.gather(run_orders(clients, expired_orders), run_server())







if __name__ == "__main__":
    asyncio.run(main())