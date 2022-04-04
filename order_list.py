"""
  order_list.py
  Description: A thread-safe queue abstraction for orders 
  Authors: Dylan Oesch-Emmel
"""
from order import Order
import threading

class OrderList:
    

    '''
        Constructor
    '''
    def __init__(self):
        self.queue = []
        self.mutex = threading.Lock()
   

    '''
        Instance Methods
    '''
    def add(self, order):
        self.mutex.acquire()
        self.queue.append(order)
        self.mutex.release()

    # returns the amount of expired orders
    # deletes expired orders from the queue
    def removeExpired(self):
        count = 0
        self.mutex.acquire()

        for i in range(len(self.queue)):
    
            if self.queue[i].expired():
                del self.queue[i]
                count += 1

        self.mutex.release()
        return count
        
           

    # deletes an order in the queue if it matches the pizza provided
    # nothing happens to the queue if no match is found
    def fulfillOrder(self, pizza):
        self.mutex.acquire()
        for i in range(len(self.queue)):

            # order in queue matches pizza provided
            if self.queue[i].fulfillOrder(pizza):

                # delete order
                del self.queue[i] 

                # release lock before returning
                self.mutex.release()
                return True, "Pizza has been served"
        # if no pizza matches an order in the queue then do nothing
        # and release lock
        self.mutex.release()
        return False, "No order matches this pizza" 
   
    # Returns a string of all the orders in the queue 
    def toString(self):
        string = ""
        self.mutex.acquire()
        for i in range(len(self.queue)):
            if not self.queue[i].expired():
                string += (self.queue[i].toString() + ", ")
        self.mutex.release()
        return string

    
    
       
    


