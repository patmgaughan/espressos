"""
  pantry.py
  Description: Holds dictionaries that describe where 
               which limitless appliances hold which ingredients 
               as well as ascii printable representations of
               ingredients

  Authors: Patrick Gaughan
"""
from appliance import *
from color import Color

class Pantry:

    # which limitless appliances hold which ingrenidents
    pantry = {
        "dough":DoughStation, 
        "sauce":Stove,
        "cheese":Fridge,
        "vegan_cheese":Fridge,
        "anchovies":Tank,
        "ham":ToppingCounter,
        "pineapple":ToppingCounter,
        "pepperoni":ToppingCounter,
        "olives":ToppingCounter,
        "onions":ToppingCounter,
        "green_peppers":ToppingCounter
    }

    # ascii looks of each ingredients
    ingredientStr = {
        "dough":Color.YELLOW + "*" + Color.reset, 
        "sauce":Color.RED + "~" + Color.reset,
        "cheese":Color.WHITE + "#" + Color.reset,
        "vegan_cheese":Color.YELLOW + "#" + Color.reset,
        "anchovies":Color.CYAN + "~" + Color.reset,

        #toppings counter
        "ham":Color.PINK + "<" + Color.reset,
        "pineapple":Color.YELLOW + ">" + Color.reset,
        "pepperoni":Color.PINK + "o" + Color.reset,
        "olives":Color.GREEN + "%" + Color.reset,
        "onions":Color.RED + "&" + Color.reset,
        "green_peppers":Color.GREEN + "{" + Color.reset,
        #end toppings counter

        "raw pizza":Color.WHITE + "@" + Color.reset,
        "pizza":Color.YELLOW + "@" + Color.reset
    }