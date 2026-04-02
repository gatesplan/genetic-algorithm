import pytest
from ff_genetic_algorithm.l0.gene_schema import GeneSchema
from ff_genetic_algorithm.l2.dna import DNA
from ff_genetic_algorithm.l4.culling_pool import CullingPool
from ff_genetic_algorithm.l4.population import PopulationPool
from ff_genetic_algorithm.l5.elite_spawner import EliteSpawner


SCHEMA = [
    GeneSchema("flag", bool),
    GeneSchema("count", int, range=(0, 100)),
    GeneSchema("ratio", float, range=(0.0, 1.0)),
]


class Trader:
    def __init__(self, dna):
        self.dna = dna
        self.scores = {}


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


class TestEliteSpawnerBasic:

    def test_spawn_returns_dna(self):
        inds = [_make(count=i, sharpe=float(i)) for i in range(10)]
        pop = _build_population(inds)
        spawner = EliteSpawner(SCHEMA, score_names=["sharpe"])
        result = spawner.spawn(pop, CullingPool())
        assert isinstance(result, DNA)

    def test_first_spawn_returns_best(self):
        inds = [_make(count=i, sharpe=float(i)) for i in range(10)]
        pop = _build_population(inds)
        spawner = EliteSpawner(SCHEMA, score_names=["sharpe"])
        dna = spawner.spawn(pop, CullingPool())
        assert dna.to_values()["count"] == 9

    def test_sequential_spawn_returns_in_rank_order(self):
        inds = [_make(count=i, sharpe=float(i)) for i in range(5)]
        pop = _build_population(inds)
        culling = CullingPool()
        spawner = EliteSpawner(SCHEMA, score_names=["sharpe"])
        results = [spawner.spawn(pop, culling).to_values()["count"] for _ in range(5)]
        assert results == [4, 3, 2, 1, 0]

    def test_wraps_around_when_exhausted(self):
        inds = [_make(count=i, sharpe=float(i)) for i in range(3)]
        pop = _build_population(inds)
        culling = CullingPool()
        spawner = EliteSpawner(SCHEMA, score_names=["sharpe"])
        results = [spawner.spawn(pop, culling).to_values()["count"] for _ in range(5)]
        assert results == [2, 1, 0, 2, 1]


class TestEliteSpawnerNoMutation:

    def test_dna_is_exact_copy(self):
        inds = [_make(count=42, ratio=0.777, sharpe=10.0)]
        pop = _build_population(inds)
        spawner = EliteSpawner(SCHEMA, score_names=["sharpe"])
        dna = spawner.spawn(pop, CullingPool())
        assert dna.to_values()["count"] == 42
        assert dna.to_values()["ratio"] == 0.777

    def test_dna_is_new_instance(self):
        inds = [_make(count=42, sharpe=10.0)]
        pop = _build_population(inds)
        spawner = EliteSpawner(SCHEMA, score_names=["sharpe"])
        dna = spawner.spawn(pop, CullingPool())
        assert dna is not inds[0].dna


class TestEliteSpawnerMultiScore:

    def test_rank_sum_composite(self):
        # sharpe: ind0=0, ind1=1, ind2=2 -> ranks 2,1,0
        # winrate: ind0=2, ind1=1, ind2=0 -> ranks 0,1,2
        # rank_sum: ind0=2, ind1=2, ind2=2 -> tie, but stable sort
        inds = [
            _make(count=0, sharpe=0.0, winrate=2.0),
            _make(count=1, sharpe=1.0, winrate=1.0),
            _make(count=2, sharpe=2.0, winrate=0.0),
        ]
        pop = _build_population(inds)
        spawner = EliteSpawner(SCHEMA, score_names=["sharpe", "winrate"])
        # all tied at rank_sum=2, so order depends on sort stability
        dna = spawner.spawn(pop, CullingPool())
        assert isinstance(dna, DNA)


class TestEliteSpawnerNewPopulationResets:

    def test_resets_on_new_population(self):
        inds1 = [_make(count=i, sharpe=float(i)) for i in range(5)]
        pop1 = _build_population(inds1)
        culling = CullingPool()
        spawner = EliteSpawner(SCHEMA, score_names=["sharpe"])
        spawner.spawn(pop1, culling)  # returns count=4
        spawner.spawn(pop1, culling)  # returns count=3

        inds2 = [_make(count=i + 10, sharpe=float(i)) for i in range(5)]
        pop2 = _build_population(inds2)
        dna = spawner.spawn(pop2, culling)  # resets, returns best of pop2
        assert dna.to_values()["count"] == 14
