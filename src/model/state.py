from enum import Enum, auto


class State(Enum):
    SUSCEPTIBLE = auto()
    EXPOSED = auto()
    INFECTED = auto()
    RESISTANT = auto()
    DEAD = auto()


def number_state(model, state):
    if(state is State.RESISTANT):
        return sum([1 for a in model.schedule.agents if a.state is not State.DEAD and len(a.resistances) > 0])
    return sum([1 for a in model.schedule.agents if a.state is state])


def number_infected(model):
    return number_state(model, State.INFECTED)


def number_susceptible(model):
    return number_state(model, State.SUSCEPTIBLE)


def number_resistant(model):
    return number_state(model, State.RESISTANT)


def number_exposed(model):
    return number_state(model, State.EXPOSED)


def number_dead(model):
    return number_state(model, State.DEAD)