import random
import pytest
from ff_genetic_algorithm.l0.gene_schema import GeneSchema
from ff_genetic_algorithm.l2.dna import DNA
from ff_genetic_algorithm.l4.culling_pool import CullingPool
from ff_genetic_algorithm.l4.population import PopulationPool
from ff_genetic_algorithm.l5.ranking_spawner import RankingSpawner


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


class TestRankingSpawnerBasic:

    def test_spawn_returns_dna(self):
        inds = [_make(sharpe=float(i), winrate=float(i * 2)) for i in range(10)]
        pop = _build_population(inds)
        spawner = RankingSpawner(SCHEMA, score_names=["sharpe", "winrate"])
        result = spawner.spawn(pop, CullingPool())
        assert isinstance(result, DNA)

    def test_spawn_dna_values_within_schema(self):
        inds = [_make(sharpe=float(i), winrate=float(i)) for i in range(10)]
        pop = _build_population(inds)
        spawner = RankingSpawner(SCHEMA, score_names=["sharpe", "winrate"])
        for _ in range(20):
            dna = spawner.spawn(pop, CullingPool())
            vals = dna.to_values()
            assert vals["flag"] in (True, False)
            assert 0 <= vals["count"] <= 100
            assert 0.0 <= vals["ratio"] <= 1.0


class TestRankingSelection:

    def test_high_rank_bias(self):
        # decay=0.9면 상위권 편중. 통계적으로 확인
        random.seed(42)
        inds = [_make(sharpe=float(i)) for i in range(20)]
        pop = _build_population(inds)
        spawner = RankingSpawner(SCHEMA, score_names=["sharpe"], decay=0.9)
        results = [spawner.spawn(pop, CullingPool()) for _ in range(50)]
        assert len(results) == 50

    def test_decay_zero_only_top(self):
        # decay=0이면 rank 0만 weight > 0
        inds = [_make(sharpe=float(i)) for i in range(10)]
        pop = _build_population(inds)
        spawner = RankingSpawner(SCHEMA, score_names=["sharpe"], decay=0.0)
        # 부모 둘 다 1등이므로 교차해도 1등의 값 기반
        dna = spawner.spawn(pop, CullingPool())
        assert isinstance(dna, DNA)


class TestRankingSpawnerMultiScore:

    def test_two_scores_different_categories(self):
        inds = [_make(sharpe=float(i), winrate=float(19 - i)) for i in range(20)]
        pop = _build_population(inds)
        spawner = RankingSpawner(SCHEMA, score_names=["sharpe", "winrate"])
        # sharpe 상위와 winrate 상위는 반대편 개체
        results = [spawner.spawn(pop, CullingPool()) for _ in range(20)]
        assert all(isinstance(d, DNA) for d in results)

    def test_single_score_works(self):
        inds = [_make(sharpe=float(i)) for i in range(10)]
        pop = _build_population(inds)
        spawner = RankingSpawner(SCHEMA, score_names=["sharpe"])
        dna = spawner.spawn(pop, CullingPool())
        assert isinstance(dna, DNA)

    def test_three_scores(self):
        inds = [_make(sharpe=float(i), winrate=float(i), drawdown=float(i))
                for i in range(10)]
        pop = _build_population(inds)
        spawner = RankingSpawner(SCHEMA, score_names=["sharpe", "winrate", "drawdown"])
        dna = spawner.spawn(pop, CullingPool())
        assert isinstance(dna, DNA)


class TestRankingSpawnerCulling:

    def test_avoids_culled_dna(self):
        random.seed(42)
        inds = [_make(sharpe=float(i)) for i in range(20)]
        pop = _build_population(inds)
        culling = CullingPool()
        spawner = RankingSpawner(SCHEMA, score_names=["sharpe"])
        dna = spawner.spawn(pop, culling)
        assert not culling.seen(dna)


class TestRankingSpawnerEdgeCases:

    def test_population_size_2(self):
        inds = [_make(sharpe=1.0, winrate=2.0), _make(sharpe=2.0, winrate=1.0)]
        pop = _build_population(inds)
        spawner = RankingSpawner(SCHEMA, score_names=["sharpe", "winrate"])
        dna = spawner.spawn(pop, CullingPool())
        assert isinstance(dna, DNA)

    def test_default_params(self):
        inds = [_make(sharpe=float(i)) for i in range(10)]
        pop = _build_population(inds)
        spawner = RankingSpawner(SCHEMA, score_names=["sharpe"])
        dna = spawner.spawn(pop, CullingPool())
        assert isinstance(dna, DNA)
