from enum import Enum, auto
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector


class State(Enum):
    SUSCEPTIBLE = auto()
    EXPOSED = auto()
    INFECTED = auto()
    RESISTANT = auto()


def number_state(model, state):
    return sum([1 for a in model.schedule.agents if a.state is state])


def number_infected(model):
    return number_state(model, State.INFECTED)


def number_susceptible(model):
    return number_state(model, State.SUSCEPTIBLE)


def number_resistant(model):
    return number_state(model, State.RESISTANT)


def number_exposed(model):
    return number_state(model, State.EXPOSED)


class CovidAgent(Agent):
    def __init__(
        self,
        unique_id,
        model,
        initial_state,
        virus_spread_chance,
        recovery_chance,
        resistance_chance,
    ):
        super().__init__(unique_id, model)
        self.initial_state = initial_state
        self.state = initial_state
        self.spread_chance = virus_spread_chance
        self.recovery_chance = recovery_chance
        self.resistance_chance = resistance_chance

    def try_to_infect(self):
        neighboring_cells = self.model.grid.get_neighbors(
            self.pos, moore=True, include_center=True
        )

        susceptible_neighbors = [
            agent for agent in neighboring_cells if agent.state == State.SUSCEPTIBLE
        ]

        for neighbor in susceptible_neighbors:
            neighbor.state = State.EXPOSED

    def try_to_recover(self):
        if self.random.random() < self.recovery_chance:
            # Agente se recuperou mas continua suscetível
            self.state = State.SUSCEPTIBLE
            # Mas ele consegue se tornar resistente?
            if self.random.random() < self.resistance_chance:
                self.state = State.RESISTANT
        else:
            # Agente continua infectado
            self.state = State.INFECTED

    def check_if_virus_developed(self):
        if self.random.random() < self.spread_chance:
            # Checa se realmente foi infectado
            self.state = State.INFECTED
        else:
            # Não foi
            self.state = State.SUSCEPTIBLE

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def step(self):

        if self.state == State.INFECTED:
            self.try_to_infect()
            self.try_to_recover()

        if self.state == State.EXPOSED:
            self.check_if_virus_developed()

        self.move()


class CovidModel(Model):
    """A toy SIR model to simulate a pandemic"""

    def __init__(
        self,
        n_susceptible,
        n_infected,
        virus_spread_chance=0.40,
        recovery_chance=0.20,
        resistance_chance=0.01,
        width=50,
        height=50,
        seed=None,
    ):
        self.num_susceptible = n_susceptible
        self.num_infected = n_infected
        self.total_agents = n_susceptible + n_infected
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.virus_spread_chance = virus_spread_chance
        self.recovery_chance = recovery_chance
        self.resistance_chance = resistance_chance

        self.running = True

        for i in range(self.total_agents):
            if i < self.num_infected:
                a = CovidAgent(
                    i,
                    self,
                    State.INFECTED,
                    self.virus_spread_chance,
                    self.recovery_chance,
                    self.resistance_chance,
                )
            else:
                a = CovidAgent(
                    i,
                    self,
                    State.SUSCEPTIBLE,
                    self.virus_spread_chance,
                    self.recovery_chance,
                    self.resistance_chance,
                )

            self.schedule.add(a)

            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

        self.datacollector = DataCollector(
            {
                "Susceptible": number_susceptible,
                "Exposed": number_exposed,
                "Infected": number_infected,
                "Resistant": number_resistant,
            }
        )

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()