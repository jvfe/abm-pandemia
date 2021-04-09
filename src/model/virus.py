from enum import Enum
from numpy import interp

class Common:
    def __init__(self, spread_chance, fatality_rate, min_time_to_recover):
        self.spread_chance = spread_chance
        self.fatality_rate = fatality_rate
        self.min_time_to_recover = min_time_to_recover


class Variant:
    def __init__(self, spread_chance, fatality_rate, min_time_to_recover, mutation_factor, variation_chance):
        self.spread_chance = spread_chance
        self.fatality_rate = fatality_rate
        self.min_time_to_recover = min_time_to_recover
        self.spread_range = spread_chance / 2
        self.fatality_range = fatality_rate / 2
        self.mutation_factor = mutation_factor
        self.variation_chance = variation_chance

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