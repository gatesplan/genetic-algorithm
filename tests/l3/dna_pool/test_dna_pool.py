import pytest
from ff_genetic_algorithm.l0.gene_schema import GeneSchema
from ff_genetic_algorithm.l0.sequence_schema import SequenceSchema
from ff_genetic_algorithm.l2.dna import DNA
from ff_genetic_algorithm.l3.dna_pool import DnaPool


SCHEMA = [
    GeneSchema("flag", bool),
    SequenceSchema("rsi", [
        GeneSchema("period", int, range=(5, 30)),
        GeneSchema("overbought", float, range=(60.0, 90.0)),
    ]),
]


class TestDnaPoolAdd:

    def test_add_dna(self):
        pool = DnaPool()
        dna = DNA(SCHEMA)
        assert pool.add(dna) is True
        assert pool.size == 1

    def test_add_duplicate_returns_false(self):
        pool = DnaPool()
        values = {"flag": True, "rsi.period": 14, "rsi.overbought": 75.0}
        dna1 = DNA(SCHEMA, values=values)
        dna2 = DNA(SCHEMA, values=values)
        assert pool.add(dna1) is True
        assert pool.add(dna2) is False
        assert pool.size == 1

    def test_add_different_dna(self):
        pool = DnaPool()
        dna1 = DNA(SCHEMA, values={"flag": True, "rsi.period": 14, "rsi.overbought": 75.0})
        dna2 = DNA(SCHEMA, values={"flag": False, "rsi.period": 20, "rsi.overbought": 80.0})
        assert pool.add(dna1) is True
        assert pool.add(dna2) is True
        assert pool.size == 2


class TestDnaPoolContains:

    def test_contains_added(self):
        pool = DnaPool()
        dna = DNA(SCHEMA, values={"flag": True, "rsi.period": 14, "rsi.overbought": 75.0})
        pool.add(dna)
        assert pool.contains(dna) is True

    def test_contains_same_values(self):
        pool = DnaPool()
        values = {"flag": True, "rsi.period": 14, "rsi.overbought": 75.0}
        dna1 = DNA(SCHEMA, values=values)
        pool.add(dna1)
        dna2 = DNA(SCHEMA, values=values)
        assert pool.contains(dna2) is True

    def test_not_contains(self):
        pool = DnaPool()
        dna1 = DNA(SCHEMA, values={"flag": True, "rsi.period": 14, "rsi.overbought": 75.0})
        dna2 = DNA(SCHEMA, values={"flag": False, "rsi.period": 20, "rsi.overbought": 80.0})
        pool.add(dna1)
        assert pool.contains(dna2) is False


class TestDnaPoolIterate:

    def test_iter(self):
        pool = DnaPool()
        dnas = [DNA(SCHEMA) for _ in range(5)]
        for d in dnas:
            pool.add(d)
        collected = list(pool)
        assert len(collected) <= 5  # some may be duplicates

    def test_empty_pool(self):
        pool = DnaPool()
        assert pool.size == 0
        assert list(pool) == []


class TestDnaPoolRemove:

    def test_remove(self):
        pool = DnaPool()
        dna = DNA(SCHEMA, values={"flag": True, "rsi.period": 14, "rsi.overbought": 75.0})
        pool.add(dna)
        assert pool.remove(dna) is True
        assert pool.size == 0
        assert pool.contains(dna) is False

    def test_remove_missing_returns_false(self):
        pool = DnaPool()
        dna = DNA(SCHEMA, values={"flag": True, "rsi.period": 14, "rsi.overbought": 75.0})
        assert pool.remove(dna) is False
