class AnimalProduct:
    any_egg = "Any Egg"
    any_milk = "Any Milk"
    brown_egg = "Egg (Brown)"
    chicken_egg = "Chicken Egg"
    cow_milk = "Cow Milk"
    dinosaur_egg_starter = "Dinosaur Egg (Starter)"
    """This item does not really exist and should never end up being displayed. 
    It's there to patch the loop in logic because of the Dinosaur-and-egg problem."""
    dinosaur_egg = "Dinosaur Egg"
    duck_egg_starter = "Duck Egg (Starter)"
    """This item does not really exist and should never end up being displayed. 
    It's there to patch the loop in logic because of the Chicken-and-egg problem."""
    duck_egg = "Duck Egg"
    duck_feather = "Duck Feather"
    egg_starter = "Egg (Starter)"
    """This item does not really exist and should never end up being displayed. 
    It's there to patch the loop in logic because of the Chicken-and-egg problem."""
    egg = "Egg"
    goat_milk = "Goat Milk"
    golden_egg_starter = "Golden Egg (Starter)"
    """This item does not really exist and should never end up being displayed. 
    It's there to patch the loop in logic because of the Chicken-and-egg problem."""
    golden_egg = "Golden Egg"
    large_brown_egg = "Large Egg (Brown)"
    large_egg = "Large Egg"
    large_goat_milk = "Large Goat Milk"
    large_milk = "Large Milk"
    milk = "Milk"
    ostrich_egg_starter = "Ostrich Egg (Starter)"
    """This item does not really exist and should never end up being displayed. 
    It's there to patch the loop in logic because of the Chicken-and-egg problem."""
    ostrich_egg = "Ostrich Egg"
    rabbit_foot = "Rabbit's Foot"
    roe = "Roe"
    slime_egg_blue = "Blue Slime Egg"
    slime_egg_green = "Green Slime Egg"
    slime_egg_purple = "Purple Slime Egg"
    slime_egg_red = "Red Slime Egg"
    slime_egg_tiger = "Tiger Slime Egg"
    squid_ink = "Squid Ink"
    truffle = "Truffle"
    void_egg_starter = "Void Egg (Starter)"
    """This item does not really exist and should never end up being displayed.
    It's there to patch the loop in logic because of the Chicken-and-egg problem."""
    void_egg = "Void Egg"
    wool = "Wool"

    @classmethod
    def specific_roe(cls, fish: str) -> str:
        return f"{cls.roe} [{fish}]"
