from ...l2.dna import DNA
from ...l4.score_ranking import rank_sum


class EliteSpawner:

    __slots__ = ('_schemas', '_score_names', '_ranked', '_idx', '_pop_key')

    def __init__(self, schemas, score_names):
        self._schemas = schemas
        self._score_names = score_names
        self._ranked = None
        self._idx = 0
        self._pop_key = None

    def spawn(self, population, culling_pool):
        pop_key = id(population)
        if self._pop_key != pop_key:
            self._pop_key = pop_key
            individuals = list(population)
            rank_scores = rank_sum(individuals, self._score_names)
            self._ranked = sorted(individuals, key=lambda i: rank_scores[id(i)])
            self._idx = 0

        ind = self._ranked[self._idx % len(self._ranked)]
        self._idx += 1
        return DNA(self._schemas, values=ind.dna.to_values())
