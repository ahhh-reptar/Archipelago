def create_filler(name: str) -> str:
    all_fillers.append(name)
    return name


def create_trap(name: str) -> str:
    all_traps.append(name)
    return name


all_fillers = []
all_traps = []


class Filler:
    starting_money = create_filler("Starting Money")


class Trap:
    spike_trap = create_filler("Spike Trap")
    meli_bomb_trap = create_filler("Meli-Bomb Trap")
    poisonous_spore_trap = create_filler("Poisonous Spore Trap")
    ink_trap = create_filler("Ink Trap")
