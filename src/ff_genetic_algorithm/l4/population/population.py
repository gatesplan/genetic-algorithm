from ...l3.dna_pool import DnaPool


class PopulationPool:

    __slots__ = ('_pool', '_individuals')

    def __init__(self):
        self._pool = DnaPool()
        self._individuals = {}

    @property
    def size(self):
        return self._pool.size

    def add(self, individual):
        dna = individual.dna
        if not self._pool.add(dna):
            return False
        self._individuals[dna.to_int()] = individual
        return True

    def get(self, dna):
        return self._individuals.get(dna.to_int())

    def sort_by(self, score_name, reverse=True):
        result = [ind for ind in self._individuals.values()
                  if score_name in ind.scores]
        result.sort(key=lambda ind: ind.scores[score_name], reverse=reverse)
        return result

    def filter_by(self, score_name, min_val=None, max_val=None):
        result = []
        for ind in self._individuals.values():
            val = ind.scores.get(score_name)
            if val is None:
                continue
            if min_val is not None and val < min_val:
                continue
            if max_val is not None and val > max_val:
                continue
            result.append(ind)
        return result

    def top(self, n, score_name):
        ranked = self.sort_by(score_name)
        return ranked[:n]

    def clear(self):
        self._pool = DnaPool()
        self._individuals.clear()

    def __iter__(self):
        return iter(self._individuals.values())

    def __len__(self):
        return self._pool.size
