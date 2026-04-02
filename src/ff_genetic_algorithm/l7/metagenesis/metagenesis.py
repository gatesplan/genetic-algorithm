from ...l5.population_filter import PopulationPurgeFilter
from ...l6.evolution_pool import EvolutionPool


class Metagenesis:

    __slots__ = ('_evolution_pool', '_purge_filter', '_purge_rules')

    def __init__(self, spawners, purge_rules):
        self._evolution_pool = EvolutionPool(spawners)
        self._purge_filter = PopulationPurgeFilter()
        self._purge_rules = list(purge_rules)

    def next(self, population, culling_pool):
        purged_pop, culling_pool = self._purge_filter.apply(
            population, culling_pool, self._purge_rules
        )
        return self._evolution_pool.evolve(purged_pop, culling_pool)
