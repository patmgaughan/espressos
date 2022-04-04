"""
  order_generator.py
  Description: The driver for producing orders and adding them to the order
               queue during the game. 
  Authors: Dylan Oesch-Emmel
"""
import time 
import sys

from order import Order
from order_list import OrderList
from pizza import Pizza

def order_generator(difficulty, order_list):
   
    # difficulty sets the rate and rate cap of orders 
    # TODO: fine tune the rates and caps
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
       
    # need start time so build_pizza can create more complex pizzas as 
    # game progresses  
    start_time = time.time()

    # loop for order making
    # TODO: figure out way to interrupt thread (exceptions doesn't work)
    #       maybe using multiprocessing and pipes??
    while True:
        pizza = Order.build_pizza(start_time) 
        order = Order(pizza)
        order_list.add(order)

        time.sleep(order_rate) 

        order_rate = order_rate * decay_rate
        if order_rate < rate_cap:
            order_rate = rate_cap
        
