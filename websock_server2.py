import threading
import time
import asyncio
import argparse
import websockets
from pprint import pprint
from player_ops import CMND_TO_FUNC
from order_list import OrderList
from order_generator import order_generator
from order import Order
from threadsafe_counter import ThreadsafeCounter


import kitchen
import cook
from color import Color

"""
Globals
"""
CONNECTIONS = 0
START = asyncio.Event()
STOP = asyncio.Event()
GAME = {}



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

async def run_orders():
    global GAME
    order_rate, decay_rate, rate_cap = choose_difficulty(GAME['difficulty'])

    # need start time so build_pizza can create more complex pizzas as
    # game progresses
    start_time = time.time()

    while not GAME['game_over'].is_set():
        pizza = Order.build_pizza(start_time)
        order = Order(pizza)
        GAME['order_list'].add(order)

        order_rate = order_rate * decay_rate

    # make sure the order_rate does not go below the rate cap
    if order_rate < rate_cap:
        order_rate = rate_cap

        GAME['expired'].add(order_list.removeExpired())

    if GAME['expired']> 1:
        game_over.set()

    for ws in GAME['output_clients']:
        await ws.send(stringGame(None, kitch, order_list, (completed_orders, expired_orders)))

    await asyncio.sleep(order_rate)



async def output_handler(websocket, start):
    global GAME
    await start.wait()
    for ws in GAME['output_clients']:
            await ws.send(stringGame(player, GAME['kitchen'], GAME['order_list'], (GAME['completed'], GAME['expired'])))

    GAME['output_clients'].append(websocket)
    while not GAME['game_over'].is_set():
        await asyncio.sleep(1)



async def input_handler(websocket, start):
    global GAME
    await start.wait()

    async with GAME['lock']:
        pos = GAME['start_position'].increment()
        player = cook.Cook(GAME['kitchen'], pos, pos, "player")

    GAME['input_clients'].append(websocket)

    while not GAME['game_over'].is_set():
        resp = await websocket.recv()

        async with GAME['lock']:

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
                    succ, msg = GAME['order_list'].fulfillOrder(pizza)
                    if succ:
                        GAME['completed'].increment()
                    else:
                        player.give(pizza)
            elif (resp == "get_"):
                succ, msg = func(arg1)
            else:
                func()

        for ws in GAME['output_clients']:
            await ws.send(stringGame(player, GAME['kitchen'], GAME['order_list'], (GAME['completed'], GAME['expired'])))






async def handler(websocket, start, stop):
    global GAME
    global CONNECTIONS

    type = await websocket.recv()
    print(f"type is {type}")
 
    CONNECTIONS += 1 
    
    print(f"Connections: {CONNECTIONS}")
    if CONNECTIONS == 2:
        print("Setting up game")
        kitch = kitchen.Kitchen()
        kitch.setUp()
        GAME['kitchen'] = kitch

        output_clients = []
        input_clients = []
        GAME['output_clients'] = output_clients
        GAME['input_clients'] = input_clients
    
        start_pos = ThreadsafeCounter()
        GAME['start_position'] = start_pos

        order_list = OrderList()
        GAME['order_list'] = order_list

        completed_orders = ThreadsafeCounter()
        expired_orders = ThreadsafeCounter()
        GAME['completed'] = completed_orders
        GAME['expired'] = expired_orders

        game_over = threading.Event()
        GAME['game_over'] = game_over
        
        lock = asyncio.Lock()
        GAME['lock'] = lock
        
        start.set()
        

 
    if type == "input":
        task = asyncio.create_task(input_handler(websocket, start))    
        await task
    elif type == "output":
        task = asyncio.create_task(output_handler(websocket, start))    
        await task


    STOP.set()


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
    parser.add_argument(
        '-d',
        type=str,
        default='easy',
        help='difficulty: hard, medium, easy',
    )

    args = parser.parse_args()
    GAME['difficulty'] = args.d
    start = asyncio.Event()
    stop = asyncio.Event()
    # wrap handler 
    handler_fun = lambda websocket: handler(websocket, start, stop)
 
    async with websockets.serve(handler_fun, args.i, args.p, ping_interval=None):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
