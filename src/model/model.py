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
        move_chance,
        recovery_chance,
        resistance_chance,
        virus=None,
    ):
        super().__init__(unique_id, model)
        self.initial_state = initial_state
        self.state = initial_state
        self.move_chance = move_chance
        self.recovery_chance = recovery_chance
        self.resistance_chance = resistance_chance
        self.virus = virus
        self.resistances = []
        self.time_infected = 0

    @property
    def virus(self):
        return self._virus

    @virus.setter
    def virus(self, value):
        # Caso seja uma variante do virus
        if isinstance(value, Variant):
            # Se ele passar no teste de mutação
            if self.random.random() < value.variation_chance:
                # É criado uma nova versão do virus com novos valores, baseados no virus original
                self._virus = Variant(
                    value.spread_chance,
                    value.fatality_rate,
                    value.min_time_to_recover,
                    self.random.uniform(-1.0, 1.0),
                    value.variation_chance,
                )
            else:
                # Senão, o virus original que é usado
                self._virus = value
            self.spread_chance = self._virus.spread_chance
            self.fatality_rate = self._virus.fatality_rate
        # Caso seja um virus comum
        elif isinstance(value, Common):
            # Usamos apenas ele mesmo
            self._virus = value
            self.spread_chance = self._virus.spread_chance
            self.fatality_rate = self._virus.fatality_rate
        else:
            self._virus = None
            self.spread_chance = 0
            self.fatality_rate = 0

    def try_to_infect(self):
        neighboring_cells = self.model.grid.get_neighbors(
            self.pos, moore=True, include_center=True
        )

        susceptible_neighbors = [
            agent for agent in neighboring_cells if agent.state == State.SUSCEPTIBLE
        ]

        for neighbor in susceptible_neighbors:
            # Caso o agente não tenha resistencia a esse virus
            if self.virus not in neighbor.resistances:
                # Ele fica exposto ao virus
                neighbor.state = State.EXPOSED
                neighbor.virus = self.virus

    def try_to_recover(self):
        # Adiciona mais uma unidade para o tempo de infecção
        self.time_infected += 1
        # Verifica se o agente já pode tentar se recuperar
        if self.time_infected >= self.virus.min_time_to_recover:
            if self.random.random() < self.recovery_chance:
                # Agente se recuperou mas continua suscetível
                self.state = State.SUSCEPTIBLE
                # Mas ele consegue se tornar resistente?
                if self.random.random() < self.resistance_chance:
                    # self.state = State.RESISTANT
                    self.resistances.append(self.virus)
                    self.virus = None
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
            if self.random.random() < self.move_chance:
                self.move()


class CovidModel(Model):
    """A toy SIR model to simulate a pandemic"""

    def __init__(
        self,
        n_susceptible,
        n_infected,
        insert_variant,
        spread_chance,
        fatality_rate,
        variation_chance,
        min_time_recovery,
        move_chance,
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
        self.move_chance = move_chance
        self.recovery_chance = recovery_chance
        self.resistance_chance = resistance_chance
        self.running = True

        if insert_variant:
            virus = Variant(
                spread_chance,
                fatality_rate,
                min_time_recovery,
                self.random.uniform(-1.0, 1.0),
                variation_chance,
            )
        else:
            virus = Common(spread_chance, fatality_rate, min_time_recovery)

        for i in range(self.total_agents):
            if i < self.num_infected:
                a = CovidAgent(
                    i,
                    self,
                    State.INFECTED,
                    self.move_chance,
                    self.recovery_chance,
                    self.resistance_chance,
                    virus,
                )

            else:
                a = CovidAgent(
                    i,
                    self,
                    State.SUSCEPTIBLE,
                    self.move_chance,
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