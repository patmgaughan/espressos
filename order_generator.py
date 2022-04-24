"""
  order_generator.py
  Description: The driver for producing orders and adding them to the order
               queue during the game. 
  Authors: Dylan Oesch-Emmel
"""
import asyncio
import websockets
import time 
import sys

from order import Order
from order_list import OrderList
from pizza import Pizza


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


# order_generator()
# Returns:  nothing, void 
# Purpose:  generate pizza orders and send them
#           to the server 
async def order_generator():
    assert len(sys.argv) == 2

    uri = "ws://localhost:8765"
    difficulty = sys.argv[1]
    order_rate, decay_rate, rate_cap = choose_difficulty(difficulty)      

    # need start time so build_pizza can create more complex pizzas as 
    # game progresses  
    start_time = time.time()

    order_list = OrderList()

    while True:
        pizza = Order.build_pizza(start_time) 
        order = Order(pizza)
        order_list.add(order)
        
        # make sure the order_rate does not go below the rate cap
        order_rate = order_rate * decay_rate
        if order_rate < rate_cap:
            order_rate = rate_cap
        
        top_five_list = order_list.topFive() 
        # must convert list into one contiguous string to send over websocket
        top_five_string = "".join(top_five) 
        async with websockets.connect(uri) as websocket:
            await websocket.send(top_five_string)

        time.sleep(order_rate) 


if __name__ == "__main__":
    asyncio.run(order_generator())
