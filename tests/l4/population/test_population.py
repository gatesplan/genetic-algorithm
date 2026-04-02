import pytest
from ff_genetic_algorithm.l0.gene_schema import GeneSchema
from ff_genetic_algorithm.l0.sequence_schema import SequenceSchema
from ff_genetic_algorithm.l2.dna import DNA
from ff_genetic_algorithm.l3.individual import Individual
from ff_genetic_algorithm.l4.population import PopulationPool


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


class TestPopulationPoolAdd:

    def test_add(self):
        pool = PopulationPool()
        ind = _make()
        assert pool.add(ind) is True
        assert pool.size == 1

    def test_add_duplicate_rejected(self):
        pool = PopulationPool()
        ind1 = _make(True, 14)
        ind2 = _make(True, 14)
        assert pool.add(ind1) is True
        assert pool.add(ind2) is False
        assert pool.size == 1

    def test_add_different(self):
        pool = PopulationPool()
        pool.add(_make(True, 14))
        pool.add(_make(False, 20))
        assert pool.size == 2


class TestPopulationPoolGet:

    def test_get_by_dna(self):
        pool = PopulationPool()
        ind = _make(True, 14, sharpe=1.5)
        pool.add(ind)
        found = pool.get(ind.dna)
        assert found is ind

    def test_get_missing_returns_none(self):
        pool = PopulationPool()
        dna = DNA(SCHEMA, values={"flag": True, "rsi.period": 14})
        assert pool.get(dna) is None


class TestPopulationPoolSortBy:

    def test_sort_by_descending(self):
        pool = PopulationPool()
        for i, period in enumerate(range(5, 10)):
            pool.add(_make(True, period, sharpe=float(i)))
        result = pool.sort_by("sharpe")
        values = [ind.scores["sharpe"] for ind in result]
        assert values == [4.0, 3.0, 2.0, 1.0, 0.0]

    def test_sort_by_ascending(self):
        pool = PopulationPool()
        for i, period in enumerate(range(5, 10)):
            pool.add(_make(True, period, mdd=float(-i)))
        result = pool.sort_by("mdd", reverse=False)
        values = [ind.scores["mdd"] for ind in result]
        assert values == [-4.0, -3.0, -2.0, -1.0, 0.0]

    def test_sort_by_excludes_missing_score(self):
        pool = PopulationPool()
        pool.add(_make(True, 14, sharpe=1.0))
        pool.add(_make(True, 15))  # no sharpe
        result = pool.sort_by("sharpe")
        assert len(result) == 1


class TestPopulationPoolFilterBy:

    def test_filter_min(self):
        pool = PopulationPool()
        pool.add(_make(True, 10, sharpe=0.5))
        pool.add(_make(True, 11, sharpe=1.5))
        pool.add(_make(True, 12, sharpe=2.5))
        result = pool.filter_by("sharpe", min_val=1.0)
        assert len(result) == 2

    def test_filter_max(self):
        pool = PopulationPool()
        pool.add(_make(True, 10, mdd=-0.5))
        pool.add(_make(True, 11, mdd=-0.2))
        pool.add(_make(True, 12, mdd=-0.05))
        result = pool.filter_by("mdd", max_val=-0.1)
        assert len(result) == 2

    def test_filter_min_and_max(self):
        pool = PopulationPool()
        pool.add(_make(True, 10, sharpe=0.5))
        pool.add(_make(True, 11, sharpe=1.5))
        pool.add(_make(True, 12, sharpe=2.5))
        result = pool.filter_by("sharpe", min_val=1.0, max_val=2.0)
        assert len(result) == 1
        assert result[0].scores["sharpe"] == 1.5

    def test_filter_excludes_missing_score(self):
        pool = PopulationPool()
        pool.add(_make(True, 10, sharpe=1.0))
        pool.add(_make(True, 11))  # no sharpe
        result = pool.filter_by("sharpe", min_val=0.0)
        assert len(result) == 1


class TestPopulationPoolTop:

    def test_top_n(self):
        pool = PopulationPool()
        for i, period in enumerate(range(5, 15)):
            pool.add(_make(True, period, sharpe=float(i)))
        top = pool.top(3, "sharpe")
        assert len(top) == 3
        values = [ind.scores["sharpe"] for ind in top]
        assert values == [9.0, 8.0, 7.0]

    def test_top_n_exceeds_size(self):
        pool = PopulationPool()
        pool.add(_make(True, 14, sharpe=1.0))
        top = pool.top(5, "sharpe")
        assert len(top) == 1


class TestPopulationPoolIterate:

    def test_iter_all(self):
        pool = PopulationPool()
        for i in range(5, 10):
            pool.add(_make(True, i))
        items = list(pool)
        assert len(items) == 5
        assert all(isinstance(ind, Individual) for ind in items)


class TestPopulationPoolClear:

    def test_clear(self):
        pool = PopulationPool()
        pool.add(_make(True, 14, sharpe=1.0))
        pool.clear()
        assert pool.size == 0
