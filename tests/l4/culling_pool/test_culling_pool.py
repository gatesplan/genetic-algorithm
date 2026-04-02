import pytest
from ff_genetic_algorithm.l0.gene_schema import GeneSchema
from ff_genetic_algorithm.l0.sequence_schema import SequenceSchema
from ff_genetic_algorithm.l2.dna import DNA
from ff_genetic_algorithm.l4.culling_pool import CullingPool


SCHEMA = [
    GeneSchema("flag", bool),
    SequenceSchema("rsi", [
        GeneSchema("period", int, range=(5, 30)),
    ]),
]

VALUES_A = {"flag": True, "rsi.period": 14}
VALUES_B = {"flag": False, "rsi.period": 20}


class TestCullingPoolMark:

    def test_mark_new_returns_true(self):
        pool = CullingPool()
        dna = DNA(SCHEMA, values=VALUES_A)
        assert pool.mark(dna) is True

    def test_mark_duplicate_returns_false(self):
        pool = CullingPool()
        dna1 = DNA(SCHEMA, values=VALUES_A)
        dna2 = DNA(SCHEMA, values=VALUES_A)
        pool.mark(dna1)
        assert pool.mark(dna2) is False

    def test_mark_different_returns_true(self):
        pool = CullingPool()
        pool.mark(DNA(SCHEMA, values=VALUES_A))
        assert pool.mark(DNA(SCHEMA, values=VALUES_B)) is True


class TestCullingPoolSeen:

    def test_seen_after_mark(self):
        pool = CullingPool()
        dna = DNA(SCHEMA, values=VALUES_A)
        pool.mark(dna)
        assert pool.seen(dna) is True

    def test_not_seen(self):
        pool = CullingPool()
        dna = DNA(SCHEMA, values=VALUES_A)
        assert pool.seen(dna) is False

    def test_seen_same_values_different_instance(self):
        pool = CullingPool()
        pool.mark(DNA(SCHEMA, values=VALUES_A))
        assert pool.seen(DNA(SCHEMA, values=VALUES_A)) is True


class TestCullingPoolAccumulation:

    def test_accumulates_across_calls(self):
        pool = CullingPool()
        for i in range(5, 15):
            dna = DNA(SCHEMA, values={"flag": True, "rsi.period": i})
            pool.mark(dna)
        assert pool.size == 10

    def test_size(self):
        pool = CullingPool()
        assert pool.size == 0
        pool.mark(DNA(SCHEMA, values=VALUES_A))
        assert pool.size == 1
        pool.mark(DNA(SCHEMA, values=VALUES_A))
        assert pool.size == 1
        pool.mark(DNA(SCHEMA, values=VALUES_B))
        assert pool.size == 2
