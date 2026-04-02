from ff_genetic_algorithm.l0.gene_schema import GeneSchema
from ff_genetic_algorithm.l2.dna import DNA
from ff_genetic_algorithm.l3.naming import dna_to_name, bits_to_name, name_to_bits, name_to_short


SCHEMA = [
    GeneSchema("flag", bool),
    GeneSchema("count", int, range=(0, 100)),
    GeneSchema("ratio", float, range=(0.0, 1.0)),
]


class TestDnaToName:

    def test_returns_string(self):
        dna = DNA(SCHEMA)
        name = dna_to_name(dna)
        assert isinstance(name, str)

    def test_all_chars_are_hangul_or_dash(self):
        dna = DNA(SCHEMA)
        name = dna_to_name(dna)
        for ch in name:
            assert ch == '-' or (0xAC00 <= ord(ch) <= 0xD7A3)

    def test_same_dna_same_name(self):
        dna = DNA(SCHEMA, values={"flag": True, "count": 50, "ratio": 0.5})
        assert dna_to_name(dna) == dna_to_name(dna)

    def test_different_dna_different_name(self):
        dna1 = DNA(SCHEMA, values={"flag": True, "count": 10, "ratio": 0.1})
        dna2 = DNA(SCHEMA, values={"flag": False, "count": 90, "ratio": 0.9})
        assert dna_to_name(dna1) != dna_to_name(dna2)


class TestRoundTrip:

    def test_bits_roundtrip(self):
        dna = DNA(SCHEMA, values={"flag": True, "count": 42, "ratio": 0.777})
        original_bits = dna.to_bits()
        name = dna_to_name(dna)
        restored = name_to_bits(name)
        assert restored[:len(original_bits)] == original_bits

    def test_bits_to_name_matches_dna_to_name(self):
        dna = DNA(SCHEMA, values={"flag": False, "count": 77, "ratio": 0.333})
        assert bits_to_name(dna.to_bits()) == dna_to_name(dna)


class TestNameToShort:

    def test_short_is_first_group(self):
        dna = DNA(SCHEMA)
        name = dna_to_name(dna)
        short = name_to_short(name)
        assert short == name.split('-')[0]

    def test_short_max_length(self):
        dna = DNA(SCHEMA)
        short = name_to_short(dna_to_name(dna))
        assert len(short) <= 8
