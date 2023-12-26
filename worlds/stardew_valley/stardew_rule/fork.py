import functools
from copy import copy
from typing import Protocol

from BaseClasses import CollectionState
from .protocol import PlayerWorldContext, StardewRule

rule_fork_cache_name = "__rule_fork_cache__"


class ForkableMethod(Protocol):
    def __call__(self, rule: StardewRule, state: CollectionState, context: PlayerWorldContext):
        ...


# In a perfect world, using the player id would be enough to copy one instance of the rule per player. However, in this world, we have tests that reuse player
#  ids... We also have to check the instance of the PlayerContext, to ensure players are different.
#  The forked is stored in the player context, so it does not memory leak. Forked rules will be garbage collected when the PlayerContext is disposed of.
def fork_per_player(stateful_method: ForkableMethod):
    # FIXME I have that this has to apply to a specific method interface :(
    @functools.wraps(stateful_method)
    def fork(rule: StardewRule, state: CollectionState, context: PlayerWorldContext):

        player_rule_fork_cache = getattr(context, rule_fork_cache_name, None)
        if player_rule_fork_cache is None:
            player_rule_fork_cache = {}
            setattr(context, rule_fork_cache_name, player_rule_fork_cache)

        try:
            forked_rule = player_rule_fork_cache[rule]
        except KeyError:
            forked_rule = copy(rule)
            player_rule_fork_cache[rule] = forked_rule

        return stateful_method(forked_rule, state, context)

    return fork
