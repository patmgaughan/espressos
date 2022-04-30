# espressos
Espressos Express: Cooking Mamas

Concurrent Final Project
Patrick, Dylan, Jackson

## How to run
### Setup
run <code>python3 -m pip install -r requirements.txt</code> to install 
dependencies

### Running
<code>python3 server.py --ip [local ip] --port [port]</code>
will run the server on the given ip and port

to connecto to the server from a client, you must be connected to the same
network and run
<code>python3 client.py --ip [local ip of server] --port [port of server] 
</code>

Once two players connect to the server, the game will begin!

## How to play
You can use the arrow keys to move your player.
<code> get </code> --> used to get ingredients from 
their appliances. If it is possible to pick up more than one 
ingredient from the appliance, such as where the toppings are,
you can specifiy the ingredient with <code> get_ingredient </code>
<code> put </code> --> used for putting ingredients
on the workstation.
<code> take </code> --> used for picking up a pizza from
the workstation.
<code> bake </code> --> used for baking a pizza in the oven.
<code> serve </code> --> used for serving the pizza. You
must be near the counter.
<code> eat </code> --> consume what you are holding
<code> duck </code> --> go duck mode
<code> dress </code> --> wear a dress
<code> hat </code> --> wear a hat
<code> miley </code> --> blue eyes


PATRICK ADD 
## Code guide
<code> appliance.py </code> --> appliances are objects that chefs can interact with
               limitless appliances allow chefs to get various
               ingredients
<code> color.py </code> --> Stores the class Color which holds constants for 
different ANSII character colors. Also holds what each game object's color is.
<code> kitchen.py </code> --> The kitchen acts as a 2D array that holds appliances
               and players. Control of kitchen mostly comes
               from chefs
<code> pizza.py </code> --> the class for the Pizza object which is used by
kitchen.py as players build pizzas. Also used by server.py because pizzas
are needed to create an order instance.
<code> server.py </code> --> DYLAN/JACKSON
<code> client.py </code> -->
<code> cook.py </code> -->
<code> order_list.py </code> -->
<code> order.py </code> -->
<code> pantry.py </code> -->
<code> player.py </code> -->
<code> sequence.py </code> -->
<code> threadsafe_counter.py </code> -->

