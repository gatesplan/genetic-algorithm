import pytest
from ff_genetic_algorithm.l0.gene_schema import GeneSchema


class TestGeneSchemaCreation:

    def test_bool_schema(self):
        s = GeneSchema("enabled", bool)
        assert s.name == "enabled"
        assert s.type is bool
        assert s.range is None
        assert s.choices is None

    def test_int_schema_with_range(self):
        s = GeneSchema("period", int, range=(5, 30))
        assert s.name == "period"
        assert s.type is int
        assert s.range == (5, 30)

    def test_float_schema_with_range(self):
        s = GeneSchema("overbought", float, range=(60.0, 90.0))
        assert s.name == "overbought"
        assert s.type is float
        assert s.range == (60.0, 90.0)

    def test_enum_schema_with_choices(self):
        s = GeneSchema("direction", choices=["long", "short", "both"])
        assert s.name == "direction"
        assert s.choices == ["long", "short", "both"]


class TestGeneSchemaValidation:

    def test_int_requires_range(self):
        with pytest.raises(ValueError):
            GeneSchema("period", int)

    def test_float_requires_range(self):
        with pytest.raises(ValueError):
            GeneSchema("std", float)

    def test_range_min_less_than_max(self):
        with pytest.raises(ValueError):
            GeneSchema("bad", int, range=(30, 5))

    def test_enum_requires_choices(self):
        with pytest.raises(ValueError):
            GeneSchema("direction")

    def test_enum_choices_not_empty(self):
        with pytest.raises(ValueError):
            GeneSchema("direction", choices=[])

    def test_bool_ignores_range(self):
        s = GeneSchema("flag", bool)
        assert s.range is None


class TestGeneSchemaCreate:

    def test_create_returns_gene(self):
        from ff_genetic_algorithm.l1.gene import Gene
        s = GeneSchema("enabled", bool)
        g = s.create()
        assert isinstance(g, Gene)
        assert g.name == "enabled"

    def test_create_with_value(self):
        s = GeneSchema("period", int, range=(5, 30))
        g = s.create(value=14)
        assert g.value == 14

    def test_create_random_within_range(self):
        s = GeneSchema("period", int, range=(5, 30))
        for _ in range(100):
            g = s.create()
            assert 5 <= g.value <= 30
