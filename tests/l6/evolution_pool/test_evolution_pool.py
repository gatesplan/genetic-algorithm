import pytest
from ff_genetic_algorithm.l0.gene_schema import GeneSchema
from ff_genetic_algorithm.l2.dna import DNA
from ff_genetic_algorithm.l4.culling_pool import CullingPool
from ff_genetic_algorithm.l4.population import PopulationPool
from ff_genetic_algorithm.l5.random_spawner import RandomSpawner
from ff_genetic_algorithm.l5.elite_spawner import EliteSpawner
from ff_genetic_algorithm.l6.evolution_pool import EvolutionPool


SCHEMA = [
    GeneSchema("flag", bool),
    GeneSchema("count", int, range=(0, 100)),
    GeneSchema("ratio", float, range=(0.0, 1.0)),
]


class Trader:
    def __init__(self, dna):
        self.dna = dna
        self.scores = {}


class FakeSpawner:
    """spawn()이 있지만 Spawner Protocol 시그니처를 만족."""
    def __init__(self, schema):
        self._schema = schema
        self._call_count = 0

    def spawn(self, population, culling_pool):
        self._call_count += 1
        while True:
            dna = DNA(self._schema)
            if not culling_pool.seen(dna):
                return dna


class NotASpawner:
    """spawn() 메서드 없음."""
    pass


def _make(flag=True, count=50, ratio=0.5, **scores):
    dna = DNA(SCHEMA, values={"flag": flag, "count": count, "ratio": ratio})
    ind = Trader(dna)
    ind.scores = dict(scores)
    return ind


def _build_population(individuals):
    pool = PopulationPool()
    for ind in individuals:
        pool.add(ind)
    return pool


class TestEvolutionPoolInit:

    def test_accepts_valid_spawners(self):
        s = FakeSpawner(SCHEMA)
        ep = EvolutionPool([(s, 5)])
        assert ep is not None

    def test_rejects_non_spawner(self):
        with pytest.raises(TypeError):
            EvolutionPool([(NotASpawner(), 5)])

    def test_accepts_multiple_spawners(self):
        s1 = FakeSpawner(SCHEMA)
        s2 = FakeSpawner(SCHEMA)
        ep = EvolutionPool([(s1, 3), (s2, 4)])
        assert ep is not None


class TestEvolutionPoolEvolve:

    def test_returns_tuple(self):
        inds = [_make(count=i, sharpe=float(i)) for i in range(5)]
        pop = _build_population(inds)
        culling = CullingPool()
        ep = EvolutionPool([(FakeSpawner(SCHEMA), 3)])
        result = ep.evolve(pop, culling)
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], PopulationPool)
        assert isinstance(result[1], CullingPool)

    def test_new_population_size_matches_total_count(self):
        inds = [_make(count=i, sharpe=float(i)) for i in range(5)]
        pop = _build_population(inds)
        culling = CullingPool()
        ep = EvolutionPool([(FakeSpawner(SCHEMA), 3), (FakeSpawner(SCHEMA), 4)])
        new_pop, _ = ep.evolve(pop, culling)
        assert new_pop.size == 7

    def test_culling_pool_is_same_object(self):
        inds = [_make(count=i, sharpe=float(i)) for i in range(5)]
        pop = _build_population(inds)
        culling = CullingPool()
        ep = EvolutionPool([(FakeSpawner(SCHEMA), 3)])
        _, returned_culling = ep.evolve(pop, culling)
        assert returned_culling is culling

    def test_spawned_dna_marked_in_culling_pool(self):
        inds = [_make(count=i, sharpe=float(i)) for i in range(5)]
        pop = _build_population(inds)
        culling = CullingPool()
        ep = EvolutionPool([(FakeSpawner(SCHEMA), 5)])
        new_pop, returned_culling = ep.evolve(pop, culling)
        for ind in new_pop:
            assert returned_culling.seen(ind.dna)

    def test_new_individuals_have_empty_scores(self):
        inds = [_make(count=i, sharpe=float(i)) for i in range(5)]
        pop = _build_population(inds)
        culling = CullingPool()
        ep = EvolutionPool([(FakeSpawner(SCHEMA), 3)])
        new_pop, _ = ep.evolve(pop, culling)
        for ind in new_pop:
            assert ind.scores == {}

    def test_culling_pool_grows(self):
        inds = [_make(count=i, sharpe=float(i)) for i in range(5)]
        pop = _build_population(inds)
        culling = CullingPool()
        ep = EvolutionPool([(FakeSpawner(SCHEMA), 4)])
        before = culling.size
        ep.evolve(pop, culling)
        assert culling.size == before + 4


class TestEvolutionPoolWithRealSpawners:

    def test_with_random_spawner(self):
        inds = [_make(count=i, sharpe=float(i)) for i in range(5)]
        pop = _build_population(inds)
        culling = CullingPool()
        ep = EvolutionPool([(RandomSpawner(SCHEMA), 5)])
        new_pop, _ = ep.evolve(pop, culling)
        assert new_pop.size == 5

    def test_with_elite_spawner(self):
        inds = [_make(count=i, sharpe=float(i)) for i in range(5)]
        pop = _build_population(inds)
        culling = CullingPool()
        ep = EvolutionPool([(EliteSpawner(SCHEMA, score_names=["sharpe"]), 3)])
        new_pop, _ = ep.evolve(pop, culling)
        assert new_pop.size == 3

    def test_mixed_spawners(self):
        inds = [_make(count=i, sharpe=float(i)) for i in range(10)]
        pop = _build_population(inds)
        culling = CullingPool()
        ep = EvolutionPool([
            (EliteSpawner(SCHEMA, score_names=["sharpe"]), 3),
            (RandomSpawner(SCHEMA), 4),
        ])
        new_pop, _ = ep.evolve(pop, culling)
        assert new_pop.size == 7
