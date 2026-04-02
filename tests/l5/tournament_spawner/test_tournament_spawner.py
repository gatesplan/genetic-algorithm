import random
import pytest
from ff_genetic_algorithm.l0.gene_schema import GeneSchema
from ff_genetic_algorithm.l2.dna import DNA
from ff_genetic_algorithm.l4.culling_pool import CullingPool
from ff_genetic_algorithm.l4.population import PopulationPool
from ff_genetic_algorithm.l5.tournament_spawner import TournamentSpawner


SCHEMA = [
    GeneSchema("flag", bool),
    GeneSchema("count", int, range=(0, 100)),
    GeneSchema("ratio", float, range=(0.0, 1.0)),
]


class Trader:
    def __init__(self, dna):
        self.dna = dna
        self.scores = {}


def _make(**scores):
    dna = DNA(SCHEMA)
    ind = Trader(dna)
    ind.scores = dict(scores)
    return ind


def _build_population(individuals):
    pool = PopulationPool()
    for ind in individuals:
        pool.add(ind)
    return pool


class TestTournamentSpawnerBasic:

    def test_spawn_returns_dna(self):
        inds = [_make(sharpe=float(i), winrate=float(i)) for i in range(10)]
        pop = _build_population(inds)
        spawner = TournamentSpawner(SCHEMA, k=3, score_names=["sharpe", "winrate"])
        result = spawner.spawn(pop, CullingPool())
        assert isinstance(result, DNA)

    def test_spawn_dna_values_within_schema(self):
        inds = [_make(sharpe=float(i)) for i in range(10)]
        pop = _build_population(inds)
        spawner = TournamentSpawner(SCHEMA, k=3, score_names=["sharpe"])
        for _ in range(20):
            dna = spawner.spawn(pop, CullingPool())
            vals = dna.to_values()
            assert vals["flag"] in (True, False)
            assert 0 <= vals["count"] <= 100
            assert 0.0 <= vals["ratio"] <= 1.0

    def test_single_score_name(self):
        inds = [_make(sharpe=float(i)) for i in range(10)]
        pop = _build_population(inds)
        spawner = TournamentSpawner(SCHEMA, k=3, score_names=["sharpe"])
        dna = spawner.spawn(pop, CullingPool())
        assert isinstance(dna, DNA)

    def test_multiple_score_names(self):
        inds = [_make(sharpe=float(i), winrate=float(9 - i)) for i in range(10)]
        pop = _build_population(inds)
        spawner = TournamentSpawner(SCHEMA, k=3, score_names=["sharpe", "winrate"])
        dna = spawner.spawn(pop, CullingPool())
        assert isinstance(dna, DNA)


class TestTournamentSelection:

    def test_higher_rank_bias(self):
        inds = [_make(sharpe=0.0)] * 9 + [_make(sharpe=100.0)]
        pop = _build_population(inds)
        spawner = TournamentSpawner(SCHEMA, k=5, score_names=["sharpe"])
        results = [spawner.spawn(pop, CullingPool()) for _ in range(10)]
        assert len(results) == 10


class TestTournamentSpawnerCulling:

    def test_avoids_culled_dna(self):
        random.seed(42)
        inds = [_make(sharpe=float(i)) for i in range(20)]
        pop = _build_population(inds)
        culling = CullingPool()
        spawner = TournamentSpawner(SCHEMA, k=3, score_names=["sharpe"])
        dna = spawner.spawn(pop, culling)
        assert not culling.seen(dna)


class TestTournamentSpawnerMutation:

    def test_no_mutation(self):
        inds = [_make(sharpe=float(i)) for i in range(10)]
        pop = _build_population(inds)
        spawner = TournamentSpawner(SCHEMA, k=3, score_names=["sharpe"], mutation_rate=0.0)
        dna = spawner.spawn(pop, CullingPool())
        assert isinstance(dna, DNA)

    def test_high_mutation(self):
        inds = [_make(sharpe=float(i)) for i in range(10)]
        pop = _build_population(inds)
        spawner = TournamentSpawner(SCHEMA, k=3, score_names=["sharpe"], mutation_rate=1.0)
        dna = spawner.spawn(pop, CullingPool())
        assert isinstance(dna, DNA)


class TestTournamentSpawnerEdgeCases:

    def test_k_equals_population(self):
        inds = [_make(sharpe=float(i)) for i in range(5)]
        pop = _build_population(inds)
        spawner = TournamentSpawner(SCHEMA, k=5, score_names=["sharpe"])
        dna = spawner.spawn(pop, CullingPool())
        assert isinstance(dna, DNA)

    def test_population_size_2(self):
        inds = [_make(sharpe=1.0), _make(sharpe=2.0)]
        pop = _build_population(inds)
        spawner = TournamentSpawner(SCHEMA, k=2, score_names=["sharpe"])
        dna = spawner.spawn(pop, CullingPool())
        assert isinstance(dna, DNA)
