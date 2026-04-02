import random
import pytest
from ff_genetic_algorithm.l0.gene_schema import GeneSchema
from ff_genetic_algorithm.l0.sequence_schema import SequenceSchema
from ff_genetic_algorithm.l2.dna import DNA
from ff_genetic_algorithm.l2.dna_ops import crossover, mutate


SCHEMA = [
    GeneSchema("flag", bool),
    GeneSchema("mode", choices=["A", "B", "C"]),
    GeneSchema("count", int, range=(0, 100)),
    GeneSchema("ratio", float, range=(0.0, 1.0)),
]

NESTED_SCHEMA = [
    GeneSchema("flag", bool),
    SequenceSchema("rsi", [
        GeneSchema("period", int, range=(5, 30)),
        GeneSchema("weight", float, range=(0.0, 2.0)),
    ]),
]


class TestCrossoverBasic:

    def test_returns_new_dna(self):
        a = DNA(SCHEMA, values={"flag": True, "mode": "A", "count": 10, "ratio": 0.1})
        b = DNA(SCHEMA, values={"flag": False, "mode": "B", "count": 90, "ratio": 0.9})
        child = crossover(a, b, SCHEMA)
        assert isinstance(child, DNA)
        assert child is not a
        assert child is not b

    def test_bool_gene_from_either_parent(self):
        a = DNA(SCHEMA, values={"flag": True, "mode": "A", "count": 50, "ratio": 0.5})
        b = DNA(SCHEMA, values={"flag": False, "mode": "A", "count": 50, "ratio": 0.5})
        results = set()
        for _ in range(100):
            child = crossover(a, b, SCHEMA)
            results.add(child.get_path("flag").value)
        assert results == {True, False}

    def test_choices_gene_from_either_parent(self):
        a = DNA(SCHEMA, values={"flag": True, "mode": "A", "count": 50, "ratio": 0.5})
        b = DNA(SCHEMA, values={"flag": True, "mode": "C", "count": 50, "ratio": 0.5})
        results = set()
        for _ in range(100):
            child = crossover(a, b, SCHEMA)
            results.add(child.get_path("mode").value)
        assert results == {"A", "C"}

    def test_int_gene_from_either_parent(self):
        a = DNA(SCHEMA, values={"flag": True, "mode": "A", "count": 10, "ratio": 0.5})
        b = DNA(SCHEMA, values={"flag": True, "mode": "A", "count": 90, "ratio": 0.5})
        results = set()
        for _ in range(100):
            child = crossover(a, b, SCHEMA)
            results.add(child.get_path("count").value)
        assert results == {10, 90}

    def test_float_gene_blx_alpha(self):
        a = DNA(SCHEMA, values={"flag": True, "mode": "A", "count": 50, "ratio": 0.2})
        b = DNA(SCHEMA, values={"flag": True, "mode": "A", "count": 50, "ratio": 0.8})
        values = []
        for _ in range(500):
            child = crossover(a, b, SCHEMA)
            values.append(child.get_path("ratio").value)
        assert min(values) < 0.2
        assert max(values) > 0.8
        assert all(0.0 <= v <= 1.0 for v in values)

    def test_float_blx_alpha_zero_no_expansion(self):
        a = DNA(SCHEMA, values={"flag": True, "mode": "A", "count": 50, "ratio": 0.3})
        b = DNA(SCHEMA, values={"flag": True, "mode": "A", "count": 50, "ratio": 0.7})
        values = []
        for _ in range(500):
            child = crossover(a, b, SCHEMA, alpha=0.0)
            values.append(child.get_path("ratio").value)
        assert all(0.3 <= v <= 0.7 for v in values)

    def test_float_same_value_parents(self):
        a = DNA(SCHEMA, values={"flag": True, "mode": "A", "count": 50, "ratio": 0.5})
        b = DNA(SCHEMA, values={"flag": True, "mode": "A", "count": 50, "ratio": 0.5})
        child = crossover(a, b, SCHEMA, alpha=0.5)
        assert 0.0 <= child.get_path("ratio").value <= 1.0


class TestCrossoverNested:

    def test_nested_schema_crossover(self):
        a = DNA(NESTED_SCHEMA, values={"flag": True, "rsi.period": 10, "rsi.weight": 0.5})
        b = DNA(NESTED_SCHEMA, values={"flag": False, "rsi.period": 25, "rsi.weight": 1.5})
        child = crossover(a, b, NESTED_SCHEMA)
        assert child.get_path("flag").value in (True, False)
        assert 5 <= child.get_path("rsi.period").value <= 30
        assert 0.0 <= child.get_path("rsi.weight").value <= 2.0


class TestMutateBasic:

    def test_returns_new_dna(self):
        dna = DNA(SCHEMA, values={"flag": True, "mode": "A", "count": 50, "ratio": 0.5})
        result = mutate(dna, SCHEMA, rate=0.0)
        assert isinstance(result, DNA)
        assert result is not dna

    def test_rate_zero_no_change(self):
        dna = DNA(SCHEMA, values={"flag": True, "mode": "A", "count": 50, "ratio": 0.5})
        result = mutate(dna, SCHEMA, rate=0.0)
        assert result.to_values() == dna.to_values()

    def test_rate_one_all_genes_may_change(self):
        random.seed(42)
        dna = DNA(SCHEMA, values={"flag": True, "mode": "A", "count": 50, "ratio": 0.5})
        changed_any = False
        for _ in range(50):
            result = mutate(dna, SCHEMA, rate=1.0)
            if result.to_values() != dna.to_values():
                changed_any = True
                break
        assert changed_any

    def test_mutated_values_within_schema_range(self):
        dna = DNA(SCHEMA, values={"flag": True, "mode": "A", "count": 50, "ratio": 0.5})
        for _ in range(100):
            result = mutate(dna, SCHEMA, rate=1.0)
            vals = result.to_values()
            assert vals["flag"] in (True, False)
            assert vals["mode"] in ("A", "B", "C")
            assert 0 <= vals["count"] <= 100
            assert 0.0 <= vals["ratio"] <= 1.0

    def test_original_dna_unchanged(self):
        dna = DNA(SCHEMA, values={"flag": True, "mode": "A", "count": 50, "ratio": 0.5})
        original = dna.to_values()
        mutate(dna, SCHEMA, rate=1.0)
        assert dna.to_values() == original


class TestMutateNested:

    def test_nested_mutation(self):
        dna = DNA(NESTED_SCHEMA, values={"flag": True, "rsi.period": 10, "rsi.weight": 0.5})
        changed_any = False
        for _ in range(50):
            result = mutate(dna, NESTED_SCHEMA, rate=1.0)
            if result.to_values() != dna.to_values():
                changed_any = True
                break
        assert changed_any

    def test_nested_values_within_range(self):
        dna = DNA(NESTED_SCHEMA, values={"flag": True, "rsi.period": 10, "rsi.weight": 0.5})
        for _ in range(100):
            result = mutate(dna, NESTED_SCHEMA, rate=1.0)
            vals = result.to_values()
            assert 5 <= vals["rsi.period"] <= 30
            assert 0.0 <= vals["rsi.weight"] <= 2.0


class TestMutateDefaultRate:

    def test_default_rate(self):
        dna = DNA(SCHEMA, values={"flag": True, "mode": "A", "count": 50, "ratio": 0.5})
        result = mutate(dna, SCHEMA)
        assert isinstance(result, DNA)
