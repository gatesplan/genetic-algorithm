import pytest
from ff_genetic_algorithm.l0.gene_schema import GeneSchema
from ff_genetic_algorithm.l0.sequence_schema import SequenceSchema


class TestSequenceSchemaCreation:

    def test_create_with_gene_schemas(self):
        s = SequenceSchema("rsi", [
            GeneSchema("enabled", bool),
            GeneSchema("period", int, range=(5, 30)),
        ])
        assert s.name == "rsi"
        assert len(s.children) == 2

    def test_nested_sequence_schema(self):
        inner = SequenceSchema("rsi", [
            GeneSchema("period", int, range=(5, 30)),
        ])
        outer = SequenceSchema("indicators", [
            inner,
            GeneSchema("weight", float, range=(0.0, 1.0)),
        ])
        assert len(outer.children) == 2
        assert isinstance(outer.children[0], SequenceSchema)
        assert isinstance(outer.children[1], GeneSchema)

    def test_order_preserved(self):
        s = SequenceSchema("group", [
            GeneSchema("a", bool),
            GeneSchema("b", bool),
            GeneSchema("c", bool),
        ])
        names = [c.name for c in s.children]
        assert names == ["a", "b", "c"]

    def test_deep_nesting(self):
        l0 = SequenceSchema("l0", [GeneSchema("x", bool)])
        l1 = SequenceSchema("l1", [l0])
        l2 = SequenceSchema("l2", [l1])
        assert l2.children[0].children[0].children[0].name == "x"


class TestSequenceSchemaValidation:

    def test_empty_children_raises(self):
        with pytest.raises(ValueError):
            SequenceSchema("empty", [])

    def test_invalid_child_type_raises(self):
        with pytest.raises(TypeError):
            SequenceSchema("bad", ["not_a_schema"])


class TestSequenceSchemaCreate:

    def test_create_returns_sequence(self):
        from ff_genetic_algorithm.l1.sequence import Sequence
        s = SequenceSchema("rsi", [
            GeneSchema("enabled", bool),
            GeneSchema("period", int, range=(5, 30)),
        ])
        seq = s.create()
        assert isinstance(seq, Sequence)
        assert seq.name == "rsi"
        assert len(seq.children) == 2

    def test_create_nested_returns_nested_sequence(self):
        from ff_genetic_algorithm.l1.sequence import Sequence
        from ff_genetic_algorithm.l1.gene import Gene
        inner = SequenceSchema("rsi", [
            GeneSchema("period", int, range=(5, 30)),
        ])
        outer = SequenceSchema("indicators", [
            inner,
            GeneSchema("weight", float, range=(0.0, 1.0)),
        ])
        seq = outer.create()
        assert isinstance(seq.children[0], Sequence)
        assert isinstance(seq.children[1], Gene)
