from cook import Cook

CMND_TO_FUNC = {"w":"moveUp", "s":"moveDown", "a":"moveLeft", "d":"moveRight",\
            "get":"commandGet", "put":"commandPut", "take":"commandTake", \
            "trash":"commandTrash", "bake":"commandBake", "serve":"commandServe", \
            "get_":"get_",\
            #new commands!
            "change hat":"toggleHat", "hat":"toggleHat",
            "wear shirt":"wearShirt", "shirt":"wearShirt",
            "wear dress":"wearDress", "dress":"wearDress",
            "miley":"mileyCyrus", "noah":"noMileyCyrus",
            "eat":"commandEat",
            "duck":"toggleDuck"}