from ...l2.dna import DNA


class RandomSpawner:

    __slots__ = ('_schemas',)

    def __init__(self, schemas):
        self._schemas = schemas

    def spawn(self, population, culling_pool):
        while True:
            dna = DNA(self._schemas)
            if not culling_pool.seen(dna):
                return dna
