from ...l3.gene_pool import GenePool


class Population:

    __slots__ = ('_pool', '_fitness')

    def __init__(self):
        self._pool = GenePool()
        self._fitness = {}

    @property
    def size(self):
        return self._pool.size

    def add(self, dna):
        if not self._pool.add(dna):
            return False
        self._fitness[dna.to_int()] = None
        return True

    def set_fitness(self, dna, fitness):
        self._fitness[dna.to_int()] = fitness

    def get_fitness(self, dna):
        return self._fitness.get(dna.to_int())

    def ranked(self):
        pairs = []
        for dna in self._pool:
            fit = self._fitness.get(dna.to_int())
            if fit is not None:
                pairs.append((dna, fit))
        pairs.sort(key=lambda x: x[1], reverse=True)
        return pairs

    def top(self, n):
        ranked = self.ranked()
        return [dna for dna, _ in ranked[:n]]

    def clear(self):
        self._pool = GenePool()
        self._fitness.clear()

    def __iter__(self):
        return iter(self._pool)

    def __len__(self):
        return self._pool.size
