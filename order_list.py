"""
  order_list.py
  Description: A thread-safe queue abstraction for orders 
  Authors: Dylan Oesch-Emmel
"""
from order import Order
from color import Color
import threading
import time

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
        
        total_orders = len(self.queue)
        # create a new list containing only the non-expired orders
        non_expired = [x for x in self.queue if not x.expired()]
        self.queue = non_expired

        expired_count = total_orders - len(self.queue)
       
        self.mutex.release()
        return expired_count
        
           

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
        return False, "Pizza has not been ordered"
   
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

        elif self.queue[index].expired():
            self.mutex.release()
            return None

        else:
            string = str(self.queue[index])
            self.mutex.release()
            return string
    
    # topFive(self)
    # Returns:  a list of strings of the first 5 orders 
    # Notes:    puts the string "Empty"  if less than 5 orders
    def topFive(self):
        topFive = []
        
        for i in range(len(self)):
            
            if len(topFive) >= 5:
                break

            string = self.orderString(i)

            if string is None:
                continue

            else:

                '''Formula -> timestamp + how long it's been waiting 
                   If it is waiting 20 secs then its green
                   If it is waiting between 20 and 35 secs then yellow'''
    
                if self.queue[i].timestamp + 20 > time.time():
                    string = Color.GREEN + string + Color.reset

                elif self.queue[i].timestamp + 35 > time.time():
                    string = Color.YELLOW + string + Color.reset
                else:
                    string = Color.RED + string + Color.reset
            
            topFive.append(string)
            
        # if there are not more than 5 orders
        while len(topFive) < 5:
            topFive.append("Empty")
        
        return topFive
                 
       
         


