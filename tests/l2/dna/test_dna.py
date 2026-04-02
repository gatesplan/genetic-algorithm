import pytest
from ff_genetic_algorithm.l0.gene_schema import GeneSchema
from ff_genetic_algorithm.l0.sequence_schema import SequenceSchema
from ff_genetic_algorithm.l1.gene import Gene
from ff_genetic_algorithm.l1.sequence import Sequence
from ff_genetic_algorithm.l2.dna import DNA


RSI_SCHEMA = SequenceSchema("rsi", [
    GeneSchema("enabled", bool),
    GeneSchema("period", int, range=(5, 30)),
    GeneSchema("overbought", float, range=(60.0, 90.0)),
])

MACD_SCHEMA = SequenceSchema("macd", [
    GeneSchema("enabled", bool),
    GeneSchema("fast", int, range=(5, 20)),
    GeneSchema("slow", int, range=(15, 50)),
])


class TestDNACreation:

    def test_create_from_schemas(self):
        dna = DNA([RSI_SCHEMA, MACD_SCHEMA])
        assert len(dna.children) == 2
        assert isinstance(dna.children[0], Sequence)
        assert isinstance(dna.children[1], Sequence)

    def test_mixed_gene_and_sequence(self):
        dna = DNA([
            GeneSchema("use_rsi", bool),
            RSI_SCHEMA,
            GeneSchema("max_trades", int, range=(1, 50)),
        ])
        assert len(dna.children) == 3
        assert isinstance(dna.children[0], Gene)
        assert isinstance(dna.children[1], Sequence)
        assert isinstance(dna.children[2], Gene)

    def test_order_preserved(self):
        dna = DNA([
            GeneSchema("a", bool),
            RSI_SCHEMA,
            GeneSchema("b", bool),
            MACD_SCHEMA,
        ])
        names = [c.name for c in dna.children]
        assert names == ["a", "rsi", "b", "macd"]


class TestDNAValues:

    def test_values_override(self):
        dna = DNA(
            [GeneSchema("period", int, range=(5, 30))],
            values={"period": 14},
        )
        assert dna.children[0].value == 14

    def test_nested_values_override(self):
        dna = DNA(
            [RSI_SCHEMA],
            values={"rsi.period": 14, "rsi.overbought": 75.0},
        )
        rsi = dna.get("rsi")
        assert rsi.get("period").value == 14
        assert rsi.get("overbought").value == 75.0

    def test_random_init_without_values(self):
        schema = GeneSchema("period", int, range=(5, 30))
        for _ in range(100):
            dna = DNA([schema])
            assert 5 <= dna.children[0].value <= 30


class TestDNAAccess:

    def test_get_top_level(self):
        dna = DNA([GeneSchema("flag", bool), RSI_SCHEMA])
        assert dna.get("flag").name == "flag"
        assert dna.get("rsi").name == "rsi"

    def test_get_missing_returns_none(self):
        dna = DNA([GeneSchema("flag", bool)])
        assert dna.get("nonexistent") is None

    def test_path_access(self):
        dna = DNA([RSI_SCHEMA])
        gene = dna.get_path("rsi.period")
        assert isinstance(gene, Gene)
        assert gene.name == "period"

    def test_path_access_deep(self):
        inner = SequenceSchema("rsi", [
            GeneSchema("period", int, range=(5, 30)),
        ])
        outer = SequenceSchema("indicators", [inner])
        dna = DNA([outer])
        gene = dna.get_path("indicators.rsi.period")
        assert gene.name == "period"

    def test_path_access_missing_returns_none(self):
        dna = DNA([RSI_SCHEMA])
        assert dna.get_path("rsi.nonexistent") is None
        assert dna.get_path("bad.path") is None


class TestDNAToValues:

    def test_top_level_gene(self):
        dna = DNA(
            [GeneSchema("flag", bool)],
            values={"flag": True},
        )
        assert dna.to_values() == {"flag": True}

    def test_nested_values(self):
        dna = DNA(
            [RSI_SCHEMA],
            values={"rsi.enabled": True, "rsi.period": 14, "rsi.overbought": 75.0},
        )
        vals = dna.to_values()
        assert vals["rsi.enabled"] is True
        assert vals["rsi.period"] == 14
        assert vals["rsi.overbought"] == 75.0

    def test_mixed(self):
        dna = DNA(
            [GeneSchema("x", bool), RSI_SCHEMA],
            values={"x": False, "rsi.period": 20},
        )
        vals = dna.to_values()
        assert vals["x"] is False
        assert vals["rsi.period"] == 20
        assert "rsi.enabled" in vals

    def test_deep_nested(self):
        inner = SequenceSchema("rsi", [
            GeneSchema("period", int, range=(5, 30)),
        ])
        outer = SequenceSchema("indicators", [inner])
        dna = DNA([outer], values={"indicators.rsi.period": 14})
        vals = dna.to_values()
        assert vals["indicators.rsi.period"] == 14


class TestDNAMigration:

    def test_migrate_add_gene(self):
        old_schemas = [RSI_SCHEMA]
        old_dna = DNA(old_schemas, values={
            "rsi.enabled": True, "rsi.period": 14, "rsi.overbought": 80.0,
        })
        old_values = old_dna.to_values()

        new_rsi = SequenceSchema("rsi", [
            GeneSchema("enabled", bool),
            GeneSchema("period", int, range=(5, 30)),
            GeneSchema("overbought", float, range=(60.0, 90.0)),
            GeneSchema("oversold", float, range=(10.0, 40.0)),  # new
        ])
        new_dna = DNA([new_rsi], values=old_values)

        assert new_dna.get_path("rsi.enabled").value is True
        assert new_dna.get_path("rsi.period").value == 14
        assert new_dna.get_path("rsi.overbought").value == 80.0
        assert 10.0 <= new_dna.get_path("rsi.oversold").value <= 40.0

    def test_migrate_remove_gene(self):
        old_dna = DNA([RSI_SCHEMA], values={
            "rsi.enabled": True, "rsi.period": 14, "rsi.overbought": 80.0,
        })
        old_values = old_dna.to_values()

        new_rsi = SequenceSchema("rsi", [
            GeneSchema("enabled", bool),
            GeneSchema("period", int, range=(5, 30)),
        ])
        new_dna = DNA([new_rsi], values=old_values)

        assert new_dna.get_path("rsi.enabled").value is True
        assert new_dna.get_path("rsi.period").value == 14

    def test_migrate_add_sequence(self):
        old_dna = DNA([RSI_SCHEMA], values={
            "rsi.enabled": True, "rsi.period": 14, "rsi.overbought": 80.0,
        })
        old_values = old_dna.to_values()

        new_dna = DNA([RSI_SCHEMA, MACD_SCHEMA], values=old_values)

        assert new_dna.get_path("rsi.period").value == 14
        assert 5 <= new_dna.get_path("macd.fast").value <= 20


class TestDNABits:

    def test_to_bits_concatenates_all_genes(self):
        dna = DNA(
            [GeneSchema("a", bool), GeneSchema("b", bool)],
            values={"a": True, "b": False},
        )
        assert dna.to_bits() == "10"

    def test_to_bits_with_sequence(self):
        schema = SequenceSchema("s", [
            GeneSchema("x", bool),
            GeneSchema("y", bool),
        ])
        dna = DNA(
            [GeneSchema("a", bool), schema],
            values={"a": True, "s.x": False, "s.y": True},
        )
        assert dna.to_bits() == "101"

    def test_to_int(self):
        dna = DNA(
            [GeneSchema("a", bool), GeneSchema("b", bool)],
            values={"a": True, "b": False},
        )
        # bits = "10" -> int = 2
        assert dna.to_int() == 2

    def test_to_int_deterministic(self):
        schemas = [RSI_SCHEMA, MACD_SCHEMA]
        values = {
            "rsi.enabled": True, "rsi.period": 14, "rsi.overbought": 75.0,
            "macd.enabled": False, "macd.fast": 10, "macd.slow": 30,
        }
        dna1 = DNA(schemas, values=values)
        dna2 = DNA(schemas, values=values)
        assert dna1.to_int() == dna2.to_int()

    def test_to_int_different_values_differ(self):
        schemas = [GeneSchema("x", int, range=(0, 7))]
        dna1 = DNA(schemas, values={"x": 3})
        dna2 = DNA(schemas, values={"x": 5})
        assert dna1.to_int() != dna2.to_int()

    def test_to_int_usable_in_set(self):
        schemas = [RSI_SCHEMA]
        pool = set()
        dna = DNA(schemas, values={
            "rsi.enabled": True, "rsi.period": 14, "rsi.overbought": 75.0,
        })
        pool.add(dna.to_int())
        dna2 = DNA(schemas, values={
            "rsi.enabled": True, "rsi.period": 14, "rsi.overbought": 75.0,
        })
        assert dna2.to_int() in pool

    def test_from_bits_roundtrip(self):
        schemas = [RSI_SCHEMA, MACD_SCHEMA]
        dna = DNA(schemas, values={
            "rsi.enabled": True, "rsi.period": 14, "rsi.overbought": 75.0,
            "macd.enabled": False, "macd.fast": 10, "macd.slow": 30,
        })
        bits = dna.to_bits()
        dna2 = DNA(schemas)
        dna2.from_bits(bits)
        assert dna.to_values() == dna2.to_values()


class TestDNAFlat:

    def test_flat_all_genes(self):
        dna = DNA([
            GeneSchema("x", bool),
            RSI_SCHEMA,
            GeneSchema("y", bool),
        ])
        flat = dna.flat()
        assert all(isinstance(g, Gene) for g in flat)
        names = [g.name for g in flat]
        assert names == ["x", "enabled", "period", "overbought", "y"]
