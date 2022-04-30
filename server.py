import threading
import time
import asyncio
import argparse
import websockets
from pprint import pprint
from player_ops import CMND_TO_FUNC
from order_list import OrderList
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

def stringGame(players, kitchen, order_list, order_counts):

    topFive = order_list.topFive()
    gamestring = ""

    for lineNum in range(0, kitchen.totalLines()):
        line = kitchen.getLine(lineNum)
        linesBefore = 4
        if(lineNum == 0):
            gamestring += line + "\n"
        elif(lineNum == 1):
            gamestring += (line + " ---------------------" + "\n")
        elif(lineNum == 2):
            gamestring += (line + "      Order Queue" + ("      Completed Orders: \033[32m{}".format(order_counts[0])) + Color.reset + "\n")
        elif(lineNum == 3):
            gamestring += (line + " ---------------------" + (" Expired Orders:   \033[91m{}".format(order_counts[1])) + Color.reset + "\n")
        elif ((lineNum - linesBefore) < 5) and ((lineNum - linesBefore) >= 0):
            gamestring += (line + str(lineNum-linesBefore+1) + ") " + topFive[lineNum - linesBefore] + "\n")
        elif(lineNum >= 10 and lineNum < 10 + len(players)):

            gamestring += line + players[lineNum - 10].inventory() + "\n"
        else:
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
    print("enteringloop")

    while not GAME['game_over'].is_set():
        pizza = Order.build_pizza(start_time)
        order = Order(pizza)
        GAME['order_list'].add(order)

        order_rate = order_rate * decay_rate
        print("inloop")

        # make sure the order_rate does not go below the rate cap
        if order_rate < rate_cap:
            order_rate = rate_cap

        GAME['expired'].add(GAME['order_list'].removeExpired())

        print(GAME['expired'].get())
        if GAME['expired'].get() > 5:
            print("GAMEOVER")
            GAME['game_over'].set()
            for ws in GAME['clients']:
                await ws.send(f"gameover")
                await ws.send(f"{GAME['completed']},{GAME['expired']}")
            break

        print("about to send")
        for ws in GAME['clients']:
            await ws.send(stringGame(GAME['players'], GAME['kitchen'], GAME['order_list'], (GAME['completed'].get(), GAME['expired'].get())))

        print("sent")
        await asyncio.sleep(order_rate)

    print("out of while")



async def output_handler(websocket, start):
    global GAME
    await start.wait()
    for ws in GAME['clients']:
            await ws.send(stringGame(GAME['players'], GAME['kitchen'], GAME['order_list'], (GAME['completed'], GAME['expired'])))

    GAME['clients'].append(websocket)
    while not GAME['game_over'].is_set():
        await asyncio.sleep(1)



async def input_handler(websocket, start):
    global GAME
    # await start.wait()

    username = await websocket.recv()

    async with GAME['lock']:
        pos = GAME['start_position'].get()
        player = cook.Cook(GAME['kitchen'], pos, pos, username)
        GAME['players'].append(player)

    GAME['clients'].append(websocket)
    for ws in GAME['clients']:
        await ws.send(stringGame(GAME['players'], GAME['kitchen'], GAME['order_list'], (GAME['completed'], GAME['expired'])))

    if len(GAME['clients']) == 2:
        for ws in GAME['clients']:
            await ws.send("start")
    for ws in GAME['clients']:
        await ws.send(stringGame(GAME['players'], GAME['kitchen'], GAME['order_list'], (GAME['completed'], GAME['expired'])))

    while not GAME['game_over'].is_set():
        resp = await websocket.recv()
        if resp == "gameover":
            break

        async with GAME['lock']:

            if (resp.startswith("get_")):
                arg1 = resp.replace('get_', '')
                resp = "get_"

            func_name = CMND_TO_FUNC.get(resp)

            if not func_name:
                await websocket.send(stringGame(GAME['players'], GAME['kitchen'], GAME['order_list'], (GAME['completed'], GAME['expired'])))
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

        for ws in GAME['clients']:
            await ws.send(stringGame(GAME['players'], GAME['kitchen'], GAME['order_list'], (GAME['completed'], GAME['expired'])))



    print("OUTOFWHILE")



async def handler(websocket, start, stop):
    global GAME
    global CONNECTIONS

    type = await websocket.recv()
    print(f"type is {type}")
 
    CONNECTIONS += 1 
   
    order_task = None 
    task = None
    print(f"Connections: {CONNECTIONS}")
    if CONNECTIONS == 1:
        print("Setting up game")
        kitch = kitchen.Kitchen()
        kitch.setUp()
        GAME['kitchen'] = kitch

        GAME['clients'] = []
        GAME['players'] = []
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

    if CONNECTIONS == 2:
        order_task = asyncio.create_task(run_orders())
        start.set()
        

 
    if type == "input":
        task = asyncio.create_task(input_handler(websocket, start))    
    elif type == "output":
        task = asyncio.create_task(output_handler(websocket, start))    

    if order_task is not None:
        print("making order task")
        await order_task
    print("about to do it")
    await task
    print("awaiting both tasks")

    CONNECTIONS -= 1
    if CONNECTIONS == 0:
        stop.set()


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
        default='hard',
        help='difficulty: hard, medium, easy',
    )

    args = parser.parse_args()
    GAME['difficulty'] = args.d
    start = asyncio.Event()
    stop = asyncio.Event()
    # wrap handler 
    handler_fun = lambda websocket: handler(websocket, start, stop)
 
    async with websockets.serve(handler_fun, args.i, args.p, ping_interval=None):
        await stop.wait()

if __name__ == "__main__":
    asyncio.run(main())
