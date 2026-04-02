import random

from ...l2.dna_ops import crossover, mutate
from ...l4.score_ranking import rank_sum


class TournamentSpawner:

    __slots__ = ('_schemas', '_k', '_score_names', '_mutation_rate', '_alpha')

    def __init__(self, schemas, k, score_names, mutation_rate=0.005, alpha=0.5):
        self._schemas = schemas
        self._k = k
        self._score_names = score_names
        self._mutation_rate = mutation_rate
        self._alpha = alpha

    def spawn(self, population, culling_pool):
        individuals = list(population)
        rank_scores = rank_sum(individuals, self._score_names)
        while True:
            p1 = self._select(individuals, rank_scores)
            p2 = self._select(individuals, rank_scores)
            child_dna = crossover(p1.dna, p2.dna, self._schemas, self._alpha)
            child_dna = mutate(child_dna, self._schemas, self._mutation_rate)
            if not culling_pool.seen(child_dna):
                return child_dna

    def _select(self, individuals, rank_scores):
        group = random.sample(individuals, min(self._k, len(individuals)))
        return min(group, key=lambda ind: rank_scores[id(ind)])
