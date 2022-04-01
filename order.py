"""
  order.py
  Description: Holds the class Order. These are displayed to the players
               and each one has a pizza to make and expired function to
               check if too much time has passed since the order was 
               placed

  Authors: Dylan Oesch-Emmel
"""
import time
import random

from pizza import Pizza


class Order:  
   
    '''
        Constants
    ''' 

    ORDER_TIME = 30
    ORDER_RATE = 30
    DECAY = .75

    FIRST_ROUND = 180
    SECOND_ROUND = 480
        
    '''
        Constructors
    '''
     
    def __init__(self):
        self.pizza = Pizza()
        
        # time() returns time in seconds since the 'epoch' 
        self.timestamp = time.time()
    
    def __init__(self, pizza):
        self.pizza = pizza
        self.timestamp = time.time()

    '''
        Instance Methods
    '''

    # expired()
    # Returns: True if order has expired
    def expired(self):
        if (time.time() - self.timestamp > ORDER_TIME): 
            return False
        else:
            return True
        
    # fulfullOrder(pizza)
    # Returns: True if the given pizza is equal to the instance's pizza
    def fulfillOrder(self, pizza):
        if (self.pizza == pizza):
            return True
        else:
            return False


    '''
        Static Methods
        -- Don't modify class or instance state
    '''

    # choose_cheese()
    # Returns: A string for vegan_cheese or regular cheese
    # Purpose: Randomly choose vegan or regular cheese
    def choose_cheese():
        vegan_cheese = random.randrange(1)
        if vegan_cheese == 1:
           return "vegan_cheese"
        else:
            return "cheese"

    # sauce_or_not()
    # Return: True if sauce is needed, False if the pizza will have no sauce 
    def sauce_or_not():
        no_sauce = random.randrange(5)
        if no_sauce == 0:
            return False
        else:
            return True         

    # choose_toppings(amount - int, anchovies - bool)
    # Returns: List of toppings for a pizza
    # Purpose: Chooses the given amount of toppings, and excludes
    #          anchovies if the given bool is False    
    def choose_toppings(amount, anchovies):
        toppings = []
        pizza_toppings = list(Pizza.possibleToppings)
        for i in range(amount):
            rand_int = random.randrange(len(pizza_toppings))
            if not anchovies:
                while pizza_toppings[rand_int] == "anchovies":
                    rand_int = random.randrange(len(pizza_toppings))
            toppings.append(pizza_toppings[rand_int])
        return toppings
    
    def build_pizza(start_time):
        
        toppings = []
       
        # Select topping amount based on how long the game has been going 
        # on for 
        if time.time() - start_time < Order.FIRST_ROUND:
            print("time diff 1: {}".format(time.time() - start_time))
            toppings = Order.choose_toppings(2, False) 
    
        elif time.time() - start_time < Order.SECOND_ROUND:
            print("time diff 2: {}".format(time.time() - start_time))
            toppings = Order.choose_toppings(3, False)
        else:
            print("time diff 3: {}".format(time.time() - start_time))
            toppings = Order.choose_toppings(5, True)

        # Pizza(sauced_bool, cheese_str, baked_bool, toppings_set)    
        return Pizza(Order.sauce_or_not(), Order.choose_cheese(), True, set(toppings))   
                    
    

def main():
    # Keep in try/finally so we can raise an exception to end the thread
    start_time = time.time()
    rate = Order.ORDER_RATE
    decay_rate = Order.DECAY
    while True:
                  
        sleep(Order.ORDER_RATE) 
        
        pizza = build_pizza(start_time) 
        order = Order(pizza)
            
    # send order to kitchen code here
    rate *= rate * ORDER.DECAY
