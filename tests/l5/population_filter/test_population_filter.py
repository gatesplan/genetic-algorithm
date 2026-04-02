import pytest
from ff_genetic_algorithm.l0.gene_schema import GeneSchema
from ff_genetic_algorithm.l0.sequence_schema import SequenceSchema
from ff_genetic_algorithm.l2.dna import DNA
from ff_genetic_algorithm.l4.culling_pool import CullingPool
from ff_genetic_algorithm.l4.population import PopulationPool
from ff_genetic_algorithm.l5.population_filter import PopulationPurgeFilter


SCHEMA = [
    GeneSchema("flag", bool),
    SequenceSchema("rsi", [
        GeneSchema("period", int, range=(5, 30)),
    ]),
]


class Trader:
    def __init__(self, dna):
        self.dna = dna
        self.scores = {}


def _make(flag=True, period=14, **scores):
    dna = DNA(SCHEMA, values={"flag": flag, "rsi.period": period})
    ind = Trader(dna)
    ind.scores = dict(scores)
    return ind


def _build_population(individuals):
    pool = PopulationPool()
    for ind in individuals:
        pool.add(ind)
    return pool


class TestPopulationFilterBasic:

    def test_single_rule_filters(self):
        inds = [
            _make(True, 10, sharpe=0.3),
            _make(True, 11, sharpe=1.5),
            _make(True, 12, sharpe=2.0),
        ]
        pop = _build_population(inds)
        culling = CullingPool()

        flt = PopulationPurgeFilter()
        result, _ = flt.apply(pop, culling, [
            lambda inds: [i for i in inds if i.scores.get("sharpe", 0) >= 1.0]
        ])
        assert result.size == 2

    def test_multiple_rules_chained(self):
        inds = [
            _make(True, i, sharpe=float(i))
            for i in range(5, 15)
        ]
        pop = _build_population(inds)
        culling = CullingPool()

        flt = PopulationPurgeFilter()
        result, _ = flt.apply(pop, culling, [
            lambda inds: [i for i in inds if i.scores["sharpe"] >= 8.0],
            lambda inds: sorted(inds, key=lambda i: i.scores["sharpe"], reverse=True)[:3],
        ])
        assert result.size == 3
        values = [ind.scores["sharpe"] for ind in result.sort_by("sharpe")]
        assert values == [14.0, 13.0, 12.0]


class TestPopulationFilterCulling:

    def test_culled_marked_in_culling_pool(self):
        inds = [
            _make(True, 10, sharpe=0.3),
            _make(True, 11, sharpe=1.5),
        ]
        pop = _build_population(inds)
        culling = CullingPool()

        flt = PopulationPurgeFilter()
        _, culling = flt.apply(pop, culling, [
            lambda inds: [i for i in inds if i.scores.get("sharpe", 0) >= 1.0]
        ])
        assert culling.seen(inds[0].dna) is True
        assert culling.seen(inds[1].dna) is False

    def test_culling_pool_accumulates(self):
        culling = CullingPool()
        flt = PopulationPurgeFilter()
        rule = lambda inds: [i for i in inds if i.scores.get("sharpe", 0) >= 1.0]

        inds1 = [_make(True, 10, sharpe=0.3), _make(True, 11, sharpe=1.5)]
        _, culling = flt.apply(_build_population(inds1), culling, [rule])

        inds2 = [_make(True, 12, sharpe=0.5), _make(True, 13, sharpe=2.0)]
        _, culling = flt.apply(_build_population(inds2), culling, [rule])

        assert culling.size == 2
        assert culling.seen(inds1[0].dna) is True
        assert culling.seen(inds2[0].dna) is True


class TestPopulationFilterEdgeCases:

    def test_empty_population(self):
        flt = PopulationPurgeFilter()
        result, _ = flt.apply(PopulationPool(), CullingPool(), [
            lambda inds: [i for i in inds if i.scores.get("sharpe", 0) >= 1.0]
        ])
        assert result.size == 0

    def test_no_rules_returns_copy(self):
        inds = [_make(True, 10, sharpe=1.0), _make(True, 11, sharpe=2.0)]
        pop = _build_population(inds)
        flt = PopulationPurgeFilter()
        result, _ = flt.apply(pop, CullingPool(), [])
        assert result.size == 2

    def test_all_culled(self):
        inds = [_make(True, 10, sharpe=0.1), _make(True, 11, sharpe=0.2)]
        pop = _build_population(inds)
        culling = CullingPool()
        flt = PopulationPurgeFilter()
        result, culling = flt.apply(pop, culling, [
            lambda inds: [i for i in inds if i.scores.get("sharpe", 0) >= 5.0]
        ])
        assert result.size == 0
        assert culling.size == 2

    def test_result_is_new_population(self):
        pop = _build_population([_make(True, 10, sharpe=1.5)])
        flt = PopulationPurgeFilter()
        result, _ = flt.apply(pop, CullingPool(), [])
        assert result is not pop
