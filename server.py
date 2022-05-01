"""
  server.py
  Description: A module containing distributed espresso's 
               express server code. Gets updates about
               orders and commands from clients. Executes
               all the game commands that are given and sents
               out a new version of the game state to
               all players when updates arrive

  Authors: Jackson Clayton
"""

import threading
import time
import asyncio
import argparse
import websockets

import kitchen
import cook
from player_ops import CMND_TO_FUNC
from order_list import OrderList
from order import Order
from threadsafe_counter import ThreadsafeCounter
from color import Color

"""
Globals
"""
CONNECTIONS = 0
GAME = {}


"""
Server Functions
"""
# stringGame()
# Returns:  the game state in a string 
# Purpose:  change the game state into a string
#           which can be displayed
def stringGame():

    topFive = GAME['order_list'].topFive()
    gamestring = "\n"
    playerPrintStart = 10
    playerPrintSize = 5

    for lineNum in range(0, GAME['kitchen'].totalLines()):
        line = GAME['kitchen'].getLine(lineNum)
        totalPlayers = len(GAME['players'])
        playerNum = (lineNum - playerPrintStart) // playerPrintSize
        # player line is between 0 and 4
        playerLine = (lineNum - playerPrintStart) % playerPrintSize

        linesBefore = 4
        if(lineNum == 0):
            gamestring += line + "\n"
        elif(lineNum == 1):
            gamestring += (line + " " + " ---------------------" + "\n")
        elif(lineNum == 2):
            gamestring += (line + " " + "      Order Queue" + 
             ("      Completed Orders: \033[32m{}".format(GAME['completed'])) +
             Color.reset + "\n")
        elif(lineNum == 3):
            gamestring += (line + " " + " ---------------------" + 
             (" Expired Orders:   \033[91m{}".format(GAME['expired'])) + 
             Color.reset + "\n")
        elif ((lineNum - linesBefore) < 5) and ((lineNum - linesBefore) >= 0):
            if(topFive[lineNum - linesBefore] == "Empty"):
                gamestring += line + "\n"
            else:
                gamestring += (line + " " + str(lineNum-linesBefore+1) + ") " 
                       + topFive[lineNum - linesBefore] + "\n")

        elif(playerNum >= 0 and playerNum < totalPlayers):

            player = GAME['players'][playerNum]
            msg = player.msgString()
            msgLen = len(msg)

            msgLine0 = ""
            msgLine1 = ""
            msgLine2 = ""
            msgLine3 = ""

            if(msgLen > 0):
                msgLine0 = "  _" + ("_" * msgLen) + "_ "
                msgLine1 = " / " + (" " * msgLen) + " \\"
                msgLine2 = "<  " + msg            + " |"
                msgLine3 = " \_" + ("_" * msgLen) + "_/"

            if(playerLine == 0):
                gamestring += line + " " + "      "              + msgLine0 + "\n"
            if(playerLine == 1):
                gamestring += line + " " + player.line1Simple() + msgLine1 + "\n"
            elif(playerLine == 2):
                gamestring += line + " " + player.line2Simple() + msgLine2 + "\n"
            elif(playerLine == 3):
                gamestring += line + " " + player.line3Simple() + msgLine3 + "\n"
            elif(playerLine == 4):
                gamestring += line + " " + player.inventory() + "\n"
        else:
            gamestring += line + "\n"

    return gamestring

# broadcast_state()
# Returns:  Nothing
# Purpose:  Sends all the clients the game state
async def broadcast_state():
    for ws in GAME['clients']:
        await ws.send(stringGame())

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

        # make sure the order_rate does not go below the rate cap
        if order_rate < rate_cap:
            order_rate = rate_cap
        
        # Add newly expired orders to our expired counter
        GAME['expired'].add(GAME['order_list'].removeExpired())

        # Game is over once there are more than 10 orders
        if GAME['expired'].get() > 10:
            GAME['game_over'].set()
            for ws in GAME['clients']:
                await ws.send(f"gameover")
                await ws.send(f"{GAME['completed']},{GAME['expired']}")
            break
        
        await broadcast_state()

        await asyncio.sleep(order_rate)




# player_handler(websocket, start)
# Returns:  Nothing
# Purpose:  Main server loop run for each client
async def player_handler(websocket, start):
    global GAME

    username = await websocket.recv()
    print(f"username: {username}")
    # Initialize a new player in a start_position
    async with GAME['lock']:
        pos = GAME['kitchen'].START_POS.pop()
        player = cook.Cook(GAME['kitchen'], pos[0], pos[1], username)
        GAME['players'].append(player)
    
    GAME['clients'].append(websocket)
    
    
    await broadcast_state() 

    # Once we have 2 clients, start the game
    if len(GAME['clients']) == 2:
        for ws in GAME['clients']:
            await ws.send("start")
    
    while not GAME['game_over'].is_set():
        
        # In order to prevent the case of waiting endlessly for a recv 
        # after the game is over, our client always signals that the game is over
        # when it is over  
        resp = await websocket.recv()
        if resp == "gameover":
            break

        async with GAME['lock']:
            
            # Parse command give and then run it
            if (resp.startswith("get_")):
                arg1 = resp.replace('get_', '')
                resp = "get_"

            func_name = CMND_TO_FUNC.get(resp)

            if not func_name:
                await websocket.send(stringGame())
                continue

            print(f"<<< {func_name}")


            func = getattr(player, func_name)

            if resp == "serve":
                succ, msg = func()
                #set player msg
                player.setMsg(msg)
                if succ:
                    pizza = player.emptyHands()
                    succ, msg = GAME['order_list'].fulfillOrder(pizza)
                    #set player msg
                    player.setMsg(msg)
                    if succ:
                        GAME['completed'].increment()
                    else:
                        player.give(pizza)

            elif (resp == "get_"):
                succ, msg = func(arg1)
                #set player msg
                player.setMsg(msg)

            else:
                succ, msg = func()
                #set player msg
                player.setMsg(msg)

        await broadcast_state() 



# handler(websocket, start, stop)
# Returns:  Nothing
# Purpose:  Handle setting up the game state, running 
#           the order task once two players have connected
#           and then starting the game
async def handler(websocket, start, stop):
    global GAME
    global CONNECTIONS

    CONNECTIONS += 1 
   
    order_task = None 
    task = None
    
    # First connection is responsible for setting up the game state
    if CONNECTIONS == 1:
        kitch = kitchen.Kitchen()
        kitch.setUp()
        GAME['kitchen'] = kitch

        GAME['clients'] = []
        GAME['players'] = []
        GAME['start_position'] = ThreadsafeCounter()

        GAME['order_list'] = OrderList()

        completed_orders = ThreadsafeCounter()
        GAME['completed'] = ThreadsafeCounter()
        GAME['expired'] = ThreadsafeCounter()
        GAME['game_over'] = asyncio.Event()
        GAME['lock'] = asyncio.Lock()

    # Second player is resonsible for creating the order task
    if CONNECTIONS == 2:
        order_task = asyncio.create_task(run_orders())
        start.set()
        

    task = asyncio.create_task(player_handler(websocket, start))    
    
    # Await tasks until they return 
    if order_task is not None:
        await order_task

    await task
    
    # Once every connection has returned from its task
    # we can signal the server to stop
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
    
    # asyncio.Event() can't be global, thus we must initialize them here
    # and wrap them with handler 
    handler_fun = lambda websocket: handler(websocket, start, stop)
 
    async with websockets.serve(handler_fun, args.i, args.p, ping_interval=None):
        await stop.wait()


if __name__ == "__main__":
    asyncio.run(main())
