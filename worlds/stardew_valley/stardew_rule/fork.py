# In a perfect world, using the player id would be enough to copy one instance of the rule per player. However, in this world, we have tests that reuse player
#  ids... We also have to check the instance of the PlayerContext, to ensure players are different.
def fork_per_player(cls):
    pass
