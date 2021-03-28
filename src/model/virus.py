from enum import Enum
from numpy import interp


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