import random

from ...l2.dna_ops import crossover, mutate


class RankingSpawner:

    __slots__ = ('_schemas', '_score_names', '_decay', '_mutation_rate', '_alpha')

    def __init__(self, schemas, score_names, decay=0.9, mutation_rate=0.005, alpha=0.5):
        self._schemas = schemas
        self._score_names = score_names
        self._decay = decay
        self._mutation_rate = mutation_rate
        self._alpha = alpha

    def spawn(self, population, culling_pool):
        individuals = list(population)
        while True:
            s1, s2 = self._pick_two_scores()
            p1 = self._select(individuals, s1)
            p2 = self._select(individuals, s2)
            child_dna = crossover(p1.dna, p2.dna, self._schemas, self._alpha)
            child_dna = mutate(child_dna, self._schemas, self._mutation_rate)
            if not culling_pool.seen(child_dna):
                return child_dna

    def _pick_two_scores(self):
        if len(self._score_names) == 1:
            return self._score_names[0], self._score_names[0]
        return random.sample(self._score_names, 2)

    def _select(self, individuals, score_name):
        ranked = sorted(individuals,
                        key=lambda ind: ind.scores.get(score_name, 0),
                        reverse=True)
        weights = [self._decay ** i for i in range(len(ranked))]
        return random.choices(ranked, weights=weights, k=1)[0]
