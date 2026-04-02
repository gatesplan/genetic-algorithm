from ...l3.individual import Individual
from ...l4.culling_pool import CullingPool
from ...l4.population import PopulationPool
from ...l5.spawner import Spawner


class _Individual:
    __slots__ = ('dna', 'scores')

    def __init__(self, dna):
        self.dna = dna
        self.scores = {}


class EvolutionPool:

    __slots__ = ('_spawners',)

    def __init__(self, spawners):
        for spawner, count in spawners:
            if not isinstance(spawner, Spawner):
                raise TypeError(f"{type(spawner).__name__} is not a Spawner")
        self._spawners = list(spawners)

    def evolve(self, population, culling_pool):
        new_pop = PopulationPool()
        for spawner, count in self._spawners:
            for _ in range(count):
                dna = spawner.spawn(population, culling_pool)
                culling_pool.mark(dna)
                new_pop.add(_Individual(dna))
        return new_pop, culling_pool
