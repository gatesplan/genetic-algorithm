import pytest
from ff_genetic_algorithm.l0.gene_schema import GeneSchema
from ff_genetic_algorithm.l0.sequence_schema import SequenceSchema
from ff_genetic_algorithm.l1.gene import Gene
from ff_genetic_algorithm.l1.sequence import Sequence


class TestSequenceCreation:

    def test_from_schema(self):
        schema = SequenceSchema("rsi", [
            GeneSchema("enabled", bool),
            GeneSchema("period", int, range=(5, 30)),
        ])
        seq = schema.create()
        assert isinstance(seq, Sequence)
        assert seq.name == "rsi"
        assert len(seq.children) == 2

    def test_order_preserved(self):
        schema = SequenceSchema("group", [
            GeneSchema("a", bool),
            GeneSchema("b", bool),
            GeneSchema("c", bool),
        ])
        seq = schema.create()
        names = [c.name for c in seq.children]
        assert names == ["a", "b", "c"]

    def test_nested_sequence(self):
        inner_schema = SequenceSchema("rsi", [
            GeneSchema("period", int, range=(5, 30)),
        ])
        outer_schema = SequenceSchema("indicators", [
            inner_schema,
            GeneSchema("weight", float, range=(0.0, 1.0)),
        ])
        seq = outer_schema.create()
        assert isinstance(seq.children[0], Sequence)
        assert isinstance(seq.children[1], Gene)
        assert seq.children[0].name == "rsi"


class TestSequenceAccess:

    def _make_seq(self):
        schema = SequenceSchema("rsi", [
            GeneSchema("enabled", bool),
            GeneSchema("period", int, range=(5, 30)),
            GeneSchema("overbought", float, range=(60.0, 90.0)),
        ])
        return schema.create()

    def test_get_by_name(self):
        seq = self._make_seq()
        gene = seq.get("period")
        assert isinstance(gene, Gene)
        assert gene.name == "period"

    def test_get_missing_returns_none(self):
        seq = self._make_seq()
        assert seq.get("nonexistent") is None

    def test_nested_get(self):
        inner = SequenceSchema("rsi", [
            GeneSchema("period", int, range=(5, 30)),
        ])
        outer = SequenceSchema("indicators", [inner])
        seq = outer.create()
        rsi = seq.get("rsi")
        assert isinstance(rsi, Sequence)
        assert rsi.get("period").name == "period"


class TestSequenceFlat:

    def test_flat_genes(self):
        inner = SequenceSchema("rsi", [
            GeneSchema("a", bool),
            GeneSchema("b", bool),
        ])
        outer = SequenceSchema("root", [
            GeneSchema("x", bool),
            inner,
            GeneSchema("y", bool),
        ])
        seq = outer.create()
        flat = seq.flat()
        assert len(flat) == 4
        names = [g.name for g in flat]
        assert names == ["x", "a", "b", "y"]
