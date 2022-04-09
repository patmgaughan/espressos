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
                return
        # if no pizza matches an order in the queue then do nothing
        # and release lock
        self.mutex.release()
   
    # Returns a string of all the orders in the queue 
    def __str__(self):
        string = ""
        self.mutex.acquire()
        for i in range(len(self.queue)):
            if not self.queue[i].expired():
                string += (str(self.queue[i]) + ", ")
        self.mutex.release()
        return string
    
    def __len__(self):
        self.mutex.acquire()
        length = len(self.queue)
        self.mutex.release()
        return length

    # orderString(index)
    # Returns:  the string of the order at index in the queue
    #           or None if index is out of bounds 
    #
    # Notes:    DOES NOT check if expired
    #           Returns None if index out of bounds
    #           Zero indexed
    def orderString(self, index):
        
        self.mutex.acquire()
        # bounds check
        if index >= len(self.queue) or index < 0:
            self.mutex.release()
            return None

        else:
            string = str(self.queue[index])
            self.mutex.release()
            return string
    
    
       
    


