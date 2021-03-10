from enum import Enum
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector


class State(Enum):
    SUSCEPTIBLE = 0
    INFECTED = 1
    RESISTANT = 2


def number_state(model, state):
    return sum([1 for a in model.schedule.agents if a.state is state])


def number_infected(model):
    return number_state(model, State.INFECTED)


def number_susceptible(model):
    return number_state(model, State.SUSCEPTIBLE)


def number_resistant(model):
    return number_state(model, State.RESISTANT)


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
            if self.random.random() < self.spread_chance:
                neighbor.state = State.INFECTED

    def try_to_change_status(self):
        if self.random.random() < self.recovery_chance:
            # Agente se recuperou mas continua suscetível
            self.state = State.SUSCEPTIBLE
            # Mas ele consegue se tornar resistente?
            if self.random.random() < self.resistance_chance:
                self.state = State.RESISTANT
        else:
            # Agente continua infectado
            self.state = State.INFECTED

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def step(self):
        if self.state == State.INFECTED:
            self.try_to_infect()
            self.try_to_change_status()

        self.move()


class CovidModel(Model):
    def __init__(
        self,
        n_susceptible,
        n_infected,
        virus_spread_chance=0.40,
        recovery_chance=0.04,
        resistance_chance=0.005,
        width=50,
        height=50,
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

        # Create agents
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
            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

        self.datacollector = DataCollector(
            {
                "Susceptible": number_susceptible,
                "Infected": number_infected,
                "Resistant": number_resistant,
            }
        )

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()