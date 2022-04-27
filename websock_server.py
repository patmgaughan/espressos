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
from color import Color





async def server(kitch, output_clients, input_clients, start_pos,
                order_list, completed_orders, expired_orders,
                game_over, lock, websocket, stop):

    type = await websocket.recv()
    print("received type")
    try:
        if type == "input":

            # TODO: add option to give username

            async with lock:
                pos = start_pos.increment()
                player = cook.Cook(kitch, pos, pos, "player")

            input_clients.append(websocket)
            while not game_over.is_set():
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
                    # check if game over
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
                for ws in output_clients:
                    await ws.send(stringGame(player, kitch, order_list, (completed_orders, expired_orders)))

        if type == "output":
            output_clients.append(websocket)
            while not game_over.is_set():
                await asyncio.sleep(1)

        #Set Future so we can end the server function
        stop.set_result(0) 

    # Once one coroutine has ended the server, another coroutine may be waiting 
    # to send data. We must catch this exception to end all other coroutines
    # that are waiting
    except websockets.exceptions.ConnectionClosedError:
        pass

def stringGame(player, kitchen, order_list, order_counts):

    topFive = order_list.topFive()
    white = Color.whiteBack + "  " + Color.reset
    black = "  "

    gamestring = ""


    for row in range(kitchen.HEIGHT):
        for j in range(1, 4):
            print(j)
            line = ""
            for col in range(kitchen.WIDTH):
                space = kitchen.at(row, col)
                if (space == None):
                    # line += "      "
                    if (j == 0 or j == 2):
                        # line += white + black + white
                        line += "      "
                    else:
                        # line += black + white + black
                        line += "      "
                else:
                    line += space.line(j)
            lineNum = (row * 3) + (j - 1)
            linesBefore = 4
            if (lineNum == 0):

                if player:
                    print(line + player.inventory())
                    gamestring += line + player.inventory() + "\n"
                else:
                    print(line)
                    gamestring += line + "\n"
            elif (lineNum == 1):
                print(line + " ---------------------")
                gamestring += line + " ---------------------" + "\n"
            elif (lineNum == 2):
                print(line + "      Order Queue")
                gamestring += line + "      Order Queue\n" #+ "      Completed Orders: \033[32m{}".format(order_counts[0]) + "\n"
            elif (lineNum == 3):
                print(line + " ---------------------") # + "\n" # " " Expired Orders:   \033[91m{}".format(order_counts[1])
                gamestring += line + " ---------------------" + "\n" # Expired Orders:   \033[91m{}".format(order_counts[1]) + "\n"
            elif ((lineNum - linesBefore) < 5) and ((lineNum - linesBefore) >= 0):
                print(line + str(lineNum-linesBefore+1) + ") "+ topFive[lineNum - linesBefore])
                gamestring += line + str(lineNum - linesBefore + 1) + ") " + topFive[lineNum - linesBefore] + "\n"
            else:
                print(line)
                gamestring += line + "\n"

    return gamestring


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
    output_clients = []
    input_clients = []
    start_pos = ThreadsafeCounter()
    order_list = OrderList()
    completed_orders = ThreadsafeCounter()
    expired_orders = ThreadsafeCounter()
    game_over = threading.Event()
    stop = asyncio.Future()
    lock = asyncio.Lock()

    #FIXME: make int immutable
    fun = lambda ws: server(kitch, output_clients, input_clients, start_pos, order_list, completed_orders,
                            expired_orders, game_over, lock, ws, stop)


    async def run_server():

        async with websockets.serve(fun, args.i, args.p, ping_interval=None):
            await stop

    async def run_orders(output_clients, expired_orders, game_over):

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

        order_rate, decay_rate, rate_cap = choose_difficulty("hard")

            # need start time so build_pizza can create more complex pizzas as
            # game progresses
        start_time = time.time()

        while not game_over.is_set():
            pizza = Order.build_pizza(start_time)
            order = Order(pizza)
            order_list.add(order)

            # make sure the order_rate does not go below the rate cap
            order_rate = order_rate * decay_rate
            if order_rate < rate_cap:
                order_rate = rate_cap

            expired_orders.add(order_list.removeExpired())

                # if endgame
                #     send out game over message and print
            if expired_orders > 1:
                game_over.set()


            for ws in output_clients:
                await ws.send(stringGame(None, kitch, order_list, (completed_orders, expired_orders)))
            await asyncio.sleep(order_rate)

    await asyncio.gather(run_orders(output_clients, expired_orders, game_over), run_server())







if __name__ == "__main__":
    asyncio.run(main())
