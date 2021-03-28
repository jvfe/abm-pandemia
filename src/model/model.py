from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from .virus import Common, Variant
from .state import (
    State,
    number_dead,
    number_infected,
    number_exposed,
    number_resistant,
    number_susceptible,
)


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
            model_reporters={
                "Susceptible": number_susceptible,
                "Exposed": number_exposed,
                "Infected": number_infected,
                "Resistant": number_resistant,
                "Dead": number_dead,
            },
            agent_reporters={
                "spread_chance": "spread_chance",
                "fatality_rate": "fatality_rate",
            },
        )

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()