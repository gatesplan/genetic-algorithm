import pytest
from ff_genetic_algorithm.l0.gene_schema import GeneSchema
from ff_genetic_algorithm.l2.dna import DNA
from ff_genetic_algorithm.l4.culling_pool import CullingPool
from ff_genetic_algorithm.l4.population import PopulationPool
from ff_genetic_algorithm.l5.random_spawner import RandomSpawner
from ff_genetic_algorithm.l5.elite_spawner import EliteSpawner
from ff_genetic_algorithm.l7.metagenesis import Metagenesis


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


def _top_half_rule(individuals):
    ranked = sorted(individuals, key=lambda i: i.scores.get("sharpe", 0), reverse=True)
    return ranked[:len(ranked) // 2]


class TestMetagenesisInit:

    def test_accepts_valid_config(self):
        mg = Metagenesis(
            spawners=[(RandomSpawner(SCHEMA), 5)],
            purge_rules=[_top_half_rule],
        )
        assert mg is not None

    def test_rejects_non_spawner(self):
        with pytest.raises(TypeError):
            Metagenesis(
                spawners=[("not_a_spawner", 5)],
                purge_rules=[],
            )


class TestMetagenesisNext:

    def test_returns_tuple(self):
        inds = [_make(count=i, sharpe=float(i)) for i in range(10)]
        pop = _build_population(inds)
        culling = CullingPool()
        mg = Metagenesis(
            spawners=[(RandomSpawner(SCHEMA), 5)],
            purge_rules=[_top_half_rule],
        )
        result = mg.next(pop, culling)
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], PopulationPool)
        assert isinstance(result[1], CullingPool)

    def test_new_population_size_matches_spawner_total(self):
        inds = [_make(count=i, sharpe=float(i)) for i in range(10)]
        pop = _build_population(inds)
        culling = CullingPool()
        mg = Metagenesis(
            spawners=[(RandomSpawner(SCHEMA), 3), (RandomSpawner(SCHEMA), 4)],
            purge_rules=[_top_half_rule],
        )
        new_pop, _ = mg.next(pop, culling)
        assert new_pop.size == 7

    def test_culling_pool_is_same_object(self):
        inds = [_make(count=i, sharpe=float(i)) for i in range(10)]
        pop = _build_population(inds)
        culling = CullingPool()
        mg = Metagenesis(
            spawners=[(RandomSpawner(SCHEMA), 5)],
            purge_rules=[_top_half_rule],
        )
        _, returned = mg.next(pop, culling)
        assert returned is culling

    def test_purged_individuals_marked_in_culling(self):
        inds = [_make(count=i, sharpe=float(i)) for i in range(10)]
        pop = _build_population(inds)
        culling = CullingPool()
        mg = Metagenesis(
            spawners=[(RandomSpawner(SCHEMA), 5)],
            purge_rules=[_top_half_rule],
        )
        mg.next(pop, culling)
        # bottom 5 (sharpe 0~4) should be marked
        for i in range(5):
            dna = DNA(SCHEMA, values={"flag": True, "count": i, "ratio": 0.5})
            assert culling.seen(dna)

    def test_new_individuals_have_empty_scores(self):
        inds = [_make(count=i, sharpe=float(i)) for i in range(10)]
        pop = _build_population(inds)
        culling = CullingPool()
        mg = Metagenesis(
            spawners=[(RandomSpawner(SCHEMA), 5)],
            purge_rules=[_top_half_rule],
        )
        new_pop, _ = mg.next(pop, culling)
        for ind in new_pop:
            assert ind.scores == {}

    def test_culling_pool_grows(self):
        inds = [_make(count=i, sharpe=float(i)) for i in range(10)]
        pop = _build_population(inds)
        culling = CullingPool()
        mg = Metagenesis(
            spawners=[(RandomSpawner(SCHEMA), 5)],
            purge_rules=[_top_half_rule],
        )
        before = culling.size
        mg.next(pop, culling)
        # purged (5) + spawned (5) = at least 10 new marks
        assert culling.size > before


class TestMetagenesisWithElite:

    def test_elite_and_random_mixed(self):
        inds = [_make(count=i, sharpe=float(i)) for i in range(10)]
        pop = _build_population(inds)
        culling = CullingPool()
        mg = Metagenesis(
            spawners=[
                (EliteSpawner(SCHEMA, score_names=["sharpe"]), 3),
                (RandomSpawner(SCHEMA), 4),
            ],
            purge_rules=[_top_half_rule],
        )
        new_pop, _ = mg.next(pop, culling)
        assert new_pop.size == 7

    def test_no_purge_rules(self):
        inds = [_make(count=i, sharpe=float(i)) for i in range(10)]
        pop = _build_population(inds)
        culling = CullingPool()
        mg = Metagenesis(
            spawners=[(RandomSpawner(SCHEMA), 5)],
            purge_rules=[],
        )
        new_pop, _ = mg.next(pop, culling)
        assert new_pop.size == 5
