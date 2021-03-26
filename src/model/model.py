from enum import Enum, auto
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from numpy import interp


class State(Enum):
    SUSCEPTIBLE = auto()
    EXPOSED = auto()
    INFECTED = auto()
    RESISTANT = auto()
    DEAD = auto()


class Variables(Enum):
    SPREAD_CHANCE = 0.40
    FATALITY_RATE = 0.024


class Common:
    def __init__(self):
        self.spread_chance = Variables.SPREAD_CHANCE.value
        self.fatality_rate = Variables.FATALITY_RATE.value


class Variant:
    def __init__(self, mutation_factor):
        self.spread_chance = Variables.SPREAD_CHANCE.value
        self.fatality_rate = Variables.FATALITY_RATE.value
        self.spread_range = Variables.SPREAD_CHANCE.value / 2
        self.fatality_range = Variables.SPREAD_CHANCE.value / 4
        self.mutation_factor = mutation_factor

    @property
    def mutation_factor(self):
        return self._mutation_factor

    @mutation_factor.setter
    def mutation_factor(self, value):
        self._mutation_factor = value

        spread_mutation = self.interp_mutation(value, self.spread_range)
        fatality_mutation = self.interp_mutation(value, self.fatality_range)

        self.spread_chance = self.spread_chance + spread_mutation
        self.fatality_rate = self.fatality_rate + fatality_mutation

    def interp_mutation(self, value, attribute):

        return interp(value, [-1, 1], [-attribute, attribute])


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


def number_dead(model):
    return number_state(model, State.DEAD)


class CovidAgent(Agent):
    def __init__(
        self,
        unique_id,
        model,
        initial_state,
        recovery_chance,
        resistance_chance,
        insert_variant=False,
    ):
        super().__init__(unique_id, model)
        self.initial_state = initial_state
        self.state = initial_state
        self.recovery_chance = recovery_chance
        self.resistance_chance = resistance_chance
        self.insert_variant = insert_variant
        self.virus = insert_variant

    @property
    def virus(self):
        return self._virus

    @virus.setter
    def virus(self, value):
        if value == True:
            self._virus = Variant(self.random.uniform(-1.0, 1.0))
            self.spread_chance = self._virus.spread_chance
            self.fatality_rate = self._virus.fatality_rate
        elif value == False:
            self._virus = Common()
            self.spread_chance = self._virus.spread_chance
            self.fatality_rate = self._virus.fatality_rate
        else:
            self._virus = None

    def try_to_infect(self):
        neighboring_cells = self.model.grid.get_neighbors(
            self.pos, moore=True, include_center=True
        )

        susceptible_neighbors = [
            agent for agent in neighboring_cells if agent.state == State.SUSCEPTIBLE
        ]

        for neighbor in susceptible_neighbors:
            neighbor.state = State.EXPOSED
            neighbor.insert_variant = self.insert_variant
            neighbor.virus = self.insert_variant

    def try_to_recover(self):
        if self.random.random() < self.recovery_chance:
            # Agente se recuperou mas continua suscetível
            self.state = State.SUSCEPTIBLE
            # Mas ele consegue se tornar resistente?
            if self.random.random() < self.resistance_chance:
                self.state = State.RESISTANT
        elif self.random.random() < self.fatality_rate:
            # Se falhou na recuperação, ver se evolui para um caso fatal
            self.state = State.DEAD
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

        if self.state != State.DEAD:
            self.move()


class CovidModel(Model):
    """A toy SIR model to simulate a pandemic"""

    def __init__(
        self,
        n_susceptible,
        n_infected,
        insert_variant,
        recovery_chance=0.2,
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
        self.recovery_chance = recovery_chance
        self.resistance_chance = resistance_chance
        self.running = True

        for i in range(self.total_agents):
            if i < self.num_infected:
                a = CovidAgent(
                    i,
                    self,
                    State.INFECTED,
                    self.recovery_chance,
                    self.resistance_chance,
                    insert_variant,
                )
            else:
                a = CovidAgent(
                    i,
                    self,
                    State.SUSCEPTIBLE,
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
                "Dead": number_dead,
            }
        )

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()