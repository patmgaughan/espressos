from ast import walk
import time
from color import Color
from random import randrange

TOTAL_HEIGHT = 22

es = [" "] * 6
es[0] = "___________                                                  /\      "
es[1] = "\_   _____/ ___________________   ____   ______ __________   )/______"
es[2] = " |    __)_ /  ___/\____ \_  __ \_/ __ \ /  ___//  ___/  _ \   /  ___/"
es[3] = " |        \\\___ \ |  |_> >  | \/\  ___/ \___ \ \___ (  <_> )  \___ \ "
es[4] = "/_______  /____  >|   __/|__|    \___  >____  >____  >____/  /____  >"
es[5] = "        \/     \/ |__|               \/     \/     \/             \/ "

esBold = [" "] * 6
esBold[0] = "███████╗░██████╗██████╗░██████╗░███████╗░██████╗░██████╗░█████╗░██╗░██████╗"
esBold[1] = "██╔════╝██╔════╝██╔══██╗██╔══██╗██╔════╝██╔════╝██╔════╝██╔══██╗╚█║██╔════╝"
esBold[2] = "█████╗░░╚█████╗░██████╔╝██████╔╝█████╗░░╚█████╗░╚█████╗░██║░░██║░╚╝╚█████╗░"
esBold[3] = "██╔══╝░░░╚═══██╗██╔═══╝░██╔══██╗██╔══╝░░░╚═══██╗░╚═══██╗██║░░██║░░░░╚═══██╗"
esBold[4] = "███████╗██████╔╝██║░░░░░██║░░██║███████╗██████╔╝██████╔╝╚█████╔╝░░░██████╔╝"
esBold[5] = "╚══════╝╚═════╝░╚═╝░░░░░╚═╝░░╚═╝╚══════╝╚═════╝░╚═════╝░░╚════╝░░░░╚═════╝░"



# ex = [" "] * 6
# ex[0] = "___________                                           "
# ex[1] = "\_   _____/__  ________________   ____   ______ ______"
# ex[2] = " |    __)_\  \/  /\____ \_  __ \_/ __ \ /  ___//  ___/"
# ex[3] = " |        \>    < |  |_> >  | \/\  ___/ \___ \ \___ \ "
# ex[4] = "/_______  /__/\_ \|   __/|__|    \___  >____  >____  >"
# ex[5] = "        \/      \/|__|               \/     \/     \/ "

exBold = [" "] * 6
exBold[0] = "███████╗██╗░░██╗██████╗░██████╗░███████╗░██████╗░██████╗"
exBold[1] = "██╔════╝╚██╗██╔╝██╔══██╗██╔══██╗██╔════╝██╔════╝██╔════╝"
exBold[2] = "█████╗░░░╚███╔╝░██████╔╝██████╔╝█████╗░░╚█████╗░╚█████╗░"
exBold[3] = "██╔══╝░░░██╔██╗░██╔═══╝░██╔══██╗██╔══╝░░░╚═══██╗░╚═══██╗"
exBold[4] = "███████╗██╔╝╚██╗██║░░░░░██║░░██║███████╗██████╔╝██████╔╝"
exBold[5] = "╚══════╝╚═╝░░╚═╝╚═╝░░░░░╚═╝░░╚═╝╚══════╝╚═════╝░╚═════╝░"

def express(ex, n):

    # ex = [" "] * 6

    ex[0] = "___________                                           "
    ex[1] = "\_   _____/__  ________________   ____   ______ ______"
    ex[2] = " |    __)_\  \/  /\____ \_  __ \_/ __ \ /  ___//  ___/"
    ex[3] = " |        \>    < |  |_> >  | \/\  ___/ \___ \ \___ \ "
    ex[4] = "/_______  /__/\_ \|   __/|__|    \___  >____  >____  >"
    ex[5] = "        \/      \/|__|               \/     \/     \/ "

    if(n == 1):
        ex[0] = "___________ "
        ex[1] = "\_   _____/ "
        ex[2] = " |    __)_  "
        ex[3] = " |        \\ "
        ex[4] = "/_______  / "
        ex[5] = "        \/  "

    if(n == 2):
        ex[0] = "___________       "
        ex[1] = "\_   _____/__  ___"
        ex[2] = " |    __)_\  \/  /"
        ex[3] = " |        \>    < "
        ex[4] = "/_______  /__/\_ \\"
        ex[5] = "        \/      \/"

    if(n == 3):
        ex[0] = "___________               "
        ex[1] = "\_   _____/__  _________  "
        ex[2] = " |    __)_\  \/  /\____ \\ "
        ex[3] = " |        \>    < |  |_> >"
        ex[4] = "/_______  /__/\_ \|   __/ "
        ex[5] = "        \/      \/|__|    "


    if(n == 4):
        ex[0] = "___________                     "
        ex[1] = "\_   _____/__  ________________ "
        ex[2] = " |    __)_\  \/  /\____ \_  __ \\"
        ex[3] = " |        \>    < |  |_> >  | \/"
        ex[4] = "/_______  /__/\_ \|   __/|__|   "
        ex[5] = "        \/      \/|__|          "

    if(n == 5):
        ex[0] = "___________                             "
        ex[1] = "\_   _____/__  ________________   ____  "
        ex[2] = " |    __)_\  \/  /\____ \_  __ \_/ __ \ "
        ex[3] = " |        \>    < |  |_> >  | \/\  ___/ "
        ex[4] = "/_______  /__/\_ \|   __/|__|    \___  >"
        ex[5] = "        \/      \/|__|               \/ "

    if(n == 6):
        ex[0] = "___________                                     "
        ex[1] = "\_   _____/__  ________________   ____   ______ "
        ex[2] = " |    __)_\  \/  /\____ \_  __ \_/ __ \ /  ___/ "
        ex[3] = " |        \>    < |  |_> >  | \/\  ___/ \___ \  "
        ex[4] = "/_______  /__/\_ \|   __/|__|    \___  >____  > "
        ex[5] = "        \/      \/|__|               \/     \/  "

    # return ex

pin = [" "] * 6

pin[0] = "__________.__       .__  /\       "
pin[1] = "\______   \__| ____ |__| )/______ "
pin[2] = " |     ___/  |/    \|  |  /  ___/ "
pin[3] = " |    |   |  |   |  \  |  \___ \  "
pin[4] = " |____|   |__|___|  /__| /____  > "
pin[5] = "                  \/          \/  "

pin2 = [" "] * 6
pin2[0] = "██████╗░██╗███╗░░██╗██╗  ██╗░██████╗"
pin2[1] = "██╔══██╗██║████╗░██║██║  ╚█║██╔════╝"
pin2[2] = "██████╔╝██║██╔██╗██║██║  ░╚╝╚█████╗░"
pin2[3] = "██╔═══╝░██║██║╚████║██║  ░░░░╚═══██╗"
pin2[4] = "██║░░░░░██║██║░╚███║██║  ░░░██████╔╝"
pin2[5] = "╚═╝░░░░░╚═╝╚═╝░░╚══╝╚═╝  ░░░╚═════╝░"

piz = [" "] * 6
# piz[0] = "__________.__                             .__        "
# piz[1] = "\______   \__|____________________ _______|__|____   "
# piz[2] = " |     ___/  \___   /\___   /\__  \\\_  __ \  \__  \  "
# piz[3] = " |    |   |  |/    /  /    /  / __ \|  | \/  |/ __ \_"
# piz[4] = " |____|   |__/_____ \/_____ \(____  /__|  |__(____  /"
# piz[5] = "                   \/      \/     \/              \/ "
piz[0] = "__________.__                            .__        "
piz[1] = "\______   \__|_______________ ___________|__|____   "
piz[2] = " |     ___/  \___   /\___   // __ \_  __ \  \__  \  "
piz[3] = " |    |   |  |/    /  /    /\  ___/|  | \/  |/ __ \_"
piz[4] = " |____|   |__/_____ \/_____ \\___  >__|  |__(____  /"
piz[5] = "                   \/      \/    \/              \/ "

pizBold = [" "] * 6
# pizBold[0] = "██████╗░██╗███████╗███████╗░█████╗░██████╗░██╗░█████╗░"
# pizBold[1] = "██╔══██╗██║╚════██║╚════██║██╔══██╗██╔══██╗██║██╔══██╗"
# pizBold[2] = "██████╔╝██║░░███╔═╝░░███╔═╝███████║██████╔╝██║███████║"
# pizBold[3] = "██╔═══╝░██║██╔══╝░░██╔══╝░░██╔══██║██╔══██╗██║██╔══██║"
# pizBold[4] = "██║░░░░░██║███████╗███████╗██║░░██║██║░░██║██║██║░░██║"
# pizBold[5] = "╚═╝░░░░░╚═╝╚══════╝╚══════╝╚═╝░░╚═╝╚═╝░░╚═╝╚═╝╚═╝░░╚═╝"

pizBold[0] = "██████╗░██╗███████╗███████╗███████╗██████╗░██╗░█████╗░"
pizBold[1] = "██╔══██╗██║╚════██║╚════██║██╔════╝██╔══██╗██║██╔══██╗"
pizBold[2] = "██████╔╝██║░░███╔═╝░░███╔═╝█████╗░░██████╔╝██║███████║"
pizBold[3] = "██╔═══╝░██║██╔══╝░░██╔══╝░░██╔══╝░░██╔══██╗██║██╔══██║"
pizBold[4] = "██║░░░░░██║███████╗███████╗███████╗██║░░██║██║██║░░██║"
pizBold[5] = "╚═╝░░░░░╚═╝╚══════╝╚══════╝╚══════╝╚═╝░░╚═╝╚═╝╚═╝░░╚═╝"

wts = [" "] * 6
wts[0] = " __      __                  __                    _________.__                 "
wts[1] = "/  \    /  \_____  ___.__. _/  |_  ____   ____    /   _____/|  |   ______  _  __"
wts[2] = "\   \/\/   /\__  \<   |  | \   __\/  _ \ /  _ \   \_____  \ |  |  /  _ \ \/ \/ /"
wts[3] = " \        /  / __ \\\___  |  |  | (  <_> |  <_> )  /        \|  |_(  <_> )     / "
wts[4] = "  \__/\  /  (____  / ____|  |__|  \____/ \____/  /_______  /|____/\____/ \/\_/  "
wts[5] = "       \/        \/\/                                    \/                    "

standingLegs = "  ||  "
walkingLegs  = "  /|  "

body = [" -[]- "] * 6  
body[0] = " -[]- "
body[1] = " -/\- "
body[2] = " -{}- "
body[3] = " -()- "
body[5] = " -[]-@"

# could definitly add to the excitment of the opening seq
def openingSeq():
    #an array of string of some size that is empty
    global es
    global standingLegs, walkingLegs

    ex = [" "] * 6
    ex[0] = "___________                                           "
    ex[1] = "\_   _____/__  ________________   ____   ______ ______"
    ex[2] = " |    __)_\  \/  /\____ \_  __ \_/ __ \ /  ___//  ___/"
    ex[3] = " |        \>    < |  |_> >  | \/\  ___/ \___ \ \___ \ "
    ex[4] = "/_______  /__/\_ \|   __/|__|    \___  >____  >____  >"
    ex[5] = "        \/      \/|__|               \/     \/     \/ "


    leftOfExpressos = 10
    rightOfExpressos = 10

    screenLength = leftOfExpressos + rightOfExpressos + len(es[0])
    print("screen length is " + str(screenLength))
    personLength = 5

    # expressPadding = (screenLength - len(ex[0])) // 2
    expressPadding = 18

    # wink
    c1 = " MmmM "
    cx = " |  | "
    c2 = " |__| "
    c3 = " (oo) "
    #c4 = " -[]- "
    c4 = body[randrange(0,5)]
    
    # standingLegs = "  ||  "
    # walkingLegs  = "  /|  "
    c5 = standingLegs

    sleepSpeed = 0.2

    frameC1 = (screenLength / 3)

    extraSpace = TOTAL_HEIGHT - 6 - 6 -  6

    for frame in range(0, screenLength - personLength):
        #print Espressos
        for j in range(0, 6):
            print((" " * leftOfExpressos) + es[j] + (" " * rightOfExpressos))

        #print Blank / Express
        if(frame >= frameC1): #Print Expressis
            if(sleepSpeed == 1):
                sleepSpeed = 0.05
            if(sleepSpeed == 0.2):
                sleepSpeed = 1
            
            express(ex, 2) #change express
            
            #decide what ex should be, either it will be between 0 
            for k in range(0, 6):
                #print("frame - frameC1 = " + str(frame - frameC1))
                num = round(frame - frameC1 + 7)
                num = num // 7
                express(ex, num)
                print((" " * expressPadding) + ex[k] + (" " * expressPadding))
        else: #Print Blank
            for k in range(0, 6):
                print(" " * screenLength)

        for i in range(0, extraSpace):
            print(" ")
        # print little guy
        print(" " * frame + c1)
        print(" " * frame + cx)
        print(" " * frame + c2)
        print(" " * frame + c3)
        print(" " * frame + c4)
        if(c5 != standingLegs):
            c5 = standingLegs
        else:
            c5 = walkingLegs
        print(" " * frame + c5)

        time.sleep(sleepSpeed)
    
    #fade to black
    for frame in range(0, TOTAL_HEIGHT):
        print(" ")
    time.sleep(0.5)

def crop(string, end):
    return string[0:end]

def closingSeq(ordersDone, ordersExpired):

    extraSpace = TOTAL_HEIGHT - 6 - 6 -  6

    global es, ex, pin, pin2, piz, pizBold, wts
    global standingLegs, walkingLegs

    esLength = len(es[0])

    # wink
    c1 = " MmmM "
    cx = " |  | "
    c2 = " |__| "
    c3 = " (oo) "
    #c4 = " -[]- "
    c4 = body[randrange(0,5)]

    w = [" "] * 4
    w[0] = "  _"
    w[1] = " / "
    w[2] = "<  "
    w[3] = " \_"

    wMiddle = [" "] * 4
    wMiddle[0] = "_"
    wMiddle[1] = " "
    wMiddle[2] = " "
    wMiddle[3] = "_"

    wEnd = [" "] * 4
    wEnd[0] = "_ "
    wEnd[1] = " \\"
    wEnd[2] = " |"
    wEnd[3] = "_/"


    msg1 = "We failed, Pini's Pizzaria has bought expresso's"
    msg2 = "We made " + Color.GREEN + str(ordersDone) + Color.reset + \
           " orders but missed " + Color.RED + str(ordersExpired) + Color.reset + " orders"
    msg2NoColor = "We made " + str(ordersDone) + " orders but missed " +  str(ordersExpired) + " orders"

    msg = msg1
    msgLen = len(msg1)

    standingLegs = "  ||  "
    walkingLegs  = "  /|  "
    c5 = standingLegs

    screenLength = 100
    # pinPadding = (screenLength - len(pin[0]) // 2)
    # pizPadding = (screenLength - len(piz[0]) // 2)
    pinPadding = 20
    pizPadding = 20

    personLength = 5

    sleepSpeed = 0.1

    frameC1 = (screenLength // 3)

    framsToFad = esLength + 18

    framePinBold = (frameC1 + framsToFad + 2)
    framePizBold = (frameC1 + framsToFad + 3)

        #fade to black
    for frame in range(0, TOTAL_HEIGHT):
        print(" ")
    time.sleep(0.2)

    screenLengthMsg = screenLength


    for frame in range(0, (frameC1 + framsToFad + 6)):

        # Change 1
        if(frame >= frameC1):
            if(sleepSpeed == 1):
                sleepSpeed = 0.05
            if(sleepSpeed == 0.2):
                sleepSpeed = 1

            # print("Espresso's / Pini's")
            for i in range(0, 6):
                if(frame > (frameC1 + framsToFad)):
                    sleepSpeed = 1
                    if(frame > framePinBold):
                        print((" " * pinPadding) + pin2[i] + (" " * pinPadding))
                    else:
                        print((" " * pinPadding) + pin[i] + (" " * pinPadding))
                else:
                    black = int(frame - frameC1 - i)
                    if(black > 0):
                        s = es[i]
                        es[i] = " " * black + s[black:]
                    print((" " * pinPadding) + es[i] + (" " * pinPadding))

            # print("Way too Slow / Pizzeria's")
            for i in range(0, 6):
                if(frame > (frameC1 + framsToFad + 1)):
                    if(frame > framePizBold):
                        print((" " * pinPadding) + pizBold[i] + (" " * pinPadding))
                    else:
                        print((" " * pinPadding) + piz[i] + (" " * pinPadding))
                    #print((" " * pinPadding) + piz[k] + (" " * pinPadding))
                else:
                    black = int(frame - frameC1 - i - 6)
                    if(black > 0):
                        s = wts[i]
                        wts[i] = " " * black + s[black:]
                    print((" " * pizPadding) + wts[i] + (" " * pizPadding))
            

        else: #Not Change 1
            for i in range(0, 6):
                print((" " * pinPadding) + es[i] + (" " * pinPadding))
            for i in range(0, 6):
                print((" " * pizPadding) + wts[i] + (" " * pizPadding))
            
        for i in range(0, extraSpace):
            print(" ")
        
        if(frame >= frameC1): #After change 1
            c5 = standingLegs
            if(frame == frameC1 + framsToFad + 5):
                c3 = " (xx) "

            if(frame == frameC1 + framsToFad + 4):
                msg = "I'm so embarrsed"
                screenLengthMsg = screenLength
                msgLen = len(msg)

            if frame == (frameC1 + (framsToFad // 2)):
                msg = msg2
                screenLengthMsg = screenLength + len(Color.RED) + len(Color.GREEN) + len(Color.reset) + len(Color.reset)
                msgLen = len(msg2NoColor)
            #for right now you will stay here
            #print("wEnd is: " + wEnd[2]) #idk why this isn't working for colorful thing
            print(crop(" " * frameC1 + c1, screenLength))
            print(crop(" " * frameC1 + cx + w[0] + (wMiddle[0] * msgLen) + wEnd[0], screenLength))
            print(crop(" " * frameC1 + c2 + w[1] + (wMiddle[1] * msgLen) + wEnd[1], screenLength))
            print(crop(" " * frameC1 + c3 + w[2] + msg + wEnd[2], screenLengthMsg))
            print(crop(" " * frameC1 + c4 + w[3] + (wMiddle[3] * msgLen) + wEnd[3], screenLength))
            print(crop(" " * frameC1 + c5, screenLength))
        else: #before Change
            if(c5 != standingLegs):
                c5 = standingLegs
            else:
                c5 = walkingLegs
            print(" " * frame + c1)
            print(" " * frame + cx)
            print(" " * frame + c2)
            print(" " * frame + c3)
            print(" " * frame + c4)
            print(" " * frame + c5)

        time.sleep(sleepSpeed)


# okay here me out
# its a kitchen room with word
# applinces inside of it
# and you just walk around the kitchen waiting
# for the other player

# once you enter the kitchen, you can't leave the kitchen
# once both players are in the kitchen, the game starts
