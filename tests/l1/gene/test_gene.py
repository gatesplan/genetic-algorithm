import pytest
from ff_genetic_algorithm.l0.gene_schema import GeneSchema
from ff_genetic_algorithm.l1.gene import Gene


class TestGeneRandomInit:

    def test_bool_random(self):
        s = GeneSchema("flag", bool)
        values = {Gene(s).value for _ in range(100)}
        assert values == {True, False}

    def test_int_random_within_range(self):
        s = GeneSchema("period", int, range=(5, 30))
        for _ in range(100):
            g = Gene(s)
            assert isinstance(g.value, int)
            assert 5 <= g.value <= 30

    def test_float_random_within_range(self):
        s = GeneSchema("pct", float, range=(1.0, 3.0))
        for _ in range(100):
            g = Gene(s)
            assert isinstance(g.value, float)
            assert 1.0 <= g.value <= 3.0

    def test_float_random_precision_3_decimals(self):
        s = GeneSchema("pct", float, range=(1.0, 3.0))
        for _ in range(100):
            g = Gene(s)
            assert g.value == round(g.value, 3)

    def test_enum_random_from_choices(self):
        s = GeneSchema("dir", choices=["long", "short", "both"])
        for _ in range(100):
            g = Gene(s)
            assert g.value in ["long", "short", "both"]


class TestGeneExplicitValue:

    def test_bool_value(self):
        s = GeneSchema("flag", bool)
        g = Gene(s, value=True)
        assert g.value is True

    def test_int_value(self):
        s = GeneSchema("period", int, range=(5, 30))
        g = Gene(s, value=14)
        assert g.value == 14

    def test_float_value(self):
        s = GeneSchema("pct", float, range=(1.0, 3.0))
        g = Gene(s, value=2.5)
        assert g.value == 2.5

    def test_float_value_rounded(self):
        s = GeneSchema("pct", float, range=(1.0, 3.0))
        g = Gene(s, value=2.12345)
        assert g.value == 2.123

    def test_enum_value(self):
        s = GeneSchema("dir", choices=["long", "short"])
        g = Gene(s, value="short")
        assert g.value == "short"


class TestGeneBits:

    def test_bool_true_to_bits(self):
        s = GeneSchema("flag", bool)
        g = Gene(s, value=True)
        assert g.to_bits() == "1"

    def test_bool_false_to_bits(self):
        s = GeneSchema("flag", bool)
        g = Gene(s, value=False)
        assert g.to_bits() == "0"

    def test_int_to_bits_and_back(self):
        s = GeneSchema("period", int, range=(5, 30))
        g = Gene(s, value=14)
        bits = g.to_bits()
        g2 = Gene(s)
        g2.from_bits(bits)
        assert g2.value == 14

    def test_int_min_to_bits(self):
        s = GeneSchema("period", int, range=(5, 30))
        g = Gene(s, value=5)
        bits = g.to_bits()
        g2 = Gene(s)
        g2.from_bits(bits)
        assert g2.value == 5

    def test_int_max_to_bits(self):
        s = GeneSchema("period", int, range=(5, 30))
        g = Gene(s, value=30)
        bits = g.to_bits()
        g2 = Gene(s)
        g2.from_bits(bits)
        assert g2.value == 30

    def test_float_to_bits_and_back(self):
        s = GeneSchema("pct", float, range=(1.0, 3.0))
        g = Gene(s, value=2.5)
        bits = g.to_bits()
        g2 = Gene(s)
        g2.from_bits(bits)
        assert g2.value == 2.5

    def test_float_precision_preserved(self):
        s = GeneSchema("pct", float, range=(1.0, 3.0))
        g = Gene(s, value=1.123)
        bits = g.to_bits()
        g2 = Gene(s)
        g2.from_bits(bits)
        assert g2.value == 1.123

    def test_enum_to_bits_and_back(self):
        s = GeneSchema("dir", choices=["long", "short", "both"])
        g = Gene(s, value="short")
        bits = g.to_bits()
        g2 = Gene(s)
        g2.from_bits(bits)
        assert g2.value == "short"

    def test_bit_length_bool(self):
        s = GeneSchema("flag", bool)
        g = Gene(s, value=True)
        assert len(g.to_bits()) == 1

    def test_bit_length_int(self):
        s = GeneSchema("period", int, range=(5, 30))
        g = Gene(s, value=14)
        # 26 steps -> 5 bits
        assert len(g.to_bits()) == 5

    def test_bit_length_float(self):
        s = GeneSchema("pct", float, range=(1.0, 3.0))
        g = Gene(s, value=2.0)
        # 2001 steps -> 11 bits
        assert len(g.to_bits()) == 11

    def test_bit_length_enum(self):
        s = GeneSchema("dir", choices=["long", "short", "both"])
        g = Gene(s, value="long")
        # 3 choices -> 2 bits
        assert len(g.to_bits()) == 2

    def test_roundtrip_all_int_values(self):
        s = GeneSchema("x", int, range=(0, 7))
        for v in range(8):
            g = Gene(s, value=v)
            bits = g.to_bits()
            g2 = Gene(s)
            g2.from_bits(bits)
            assert g2.value == v


class TestFromBitsOverflow:
    """bit representation range > value range -> clamp to valid range"""

    def test_int_overflow_clamped_to_max(self):
        # range(5, 30) -> 26 steps, 5 bits, max idx = 31
        s = GeneSchema("period", int, range=(5, 30))
        g = Gene(s, value=5)
        g.from_bits("11111")  # idx=31, should clamp to 25 -> value=30
        assert g.value == 30

    def test_int_overflow_just_above(self):
        s = GeneSchema("period", int, range=(5, 30))
        g = Gene(s, value=5)
        g.from_bits("11010")  # idx=26, just outside -> clamp to 25 -> value=30
        assert g.value == 30

    def test_choices_overflow_clamped_to_last(self):
        # 3 choices -> 2 bits, max idx = 3
        s = GeneSchema("dir", choices=["long", "short", "both"])
        g = Gene(s, value="long")
        g.from_bits("11")  # idx=3, only 0-2 valid -> clamp to 2 -> "both"
        assert g.value == "both"

    def test_float_overflow_clamped_to_max(self):
        # range(1.0, 3.0) -> 2001 steps, 11 bits, max idx = 2047
        s = GeneSchema("pct", float, range=(1.0, 3.0))
        g = Gene(s, value=1.0)
        g.from_bits("11111111111")  # idx=2047, max valid=2000 -> clamp
        assert g.value == 3.0

    def test_int_within_range_unchanged(self):
        s = GeneSchema("period", int, range=(5, 30))
        g = Gene(s, value=5)
        g.from_bits("01001")  # idx=9 -> value=14, valid
        assert g.value == 14

    def test_bool_no_overflow(self):
        # 1 bit, 2 values -> no overflow possible
        s = GeneSchema("flag", bool)
        g = Gene(s, value=False)
        g.from_bits("1")
        assert g.value is True


class TestGeneProperties:

    def test_name_from_schema(self):
        s = GeneSchema("period", int, range=(5, 30))
        g = Gene(s)
        assert g.name == "period"

    def test_schema_reference(self):
        s = GeneSchema("flag", bool)
        g = Gene(s)
        assert g.schema is s
