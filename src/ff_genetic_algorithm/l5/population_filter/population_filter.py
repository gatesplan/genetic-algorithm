from ...l4.population import PopulationPool


class PopulationPurgeFilter:

    __slots__ = ()

    def apply(self, population, culling_pool, rules):
        survivors = list(population)
        for rule in rules:
            survivors = rule(survivors)

        survivor_keys = {ind.dna.to_int() for ind in survivors}
        for ind in population:
            if ind.dna.to_int() not in survivor_keys:
                culling_pool.mark(ind.dna)

        new_pop = PopulationPool()
        for ind in survivors:
            new_pop.add(ind)
        return new_pop, culling_pool
