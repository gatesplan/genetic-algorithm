import pytest
from ff_genetic_algorithm.l0.gene_schema import GeneSchema
from ff_genetic_algorithm.l0.sequence_schema import SequenceSchema
from ff_genetic_algorithm.l2.dna import DNA
from ff_genetic_algorithm.l3.individual import Individual


SCHEMA = [
    GeneSchema("flag", bool),
    SequenceSchema("rsi", [
        GeneSchema("period", int, range=(5, 30)),
    ]),
]


def _make_dna(flag=True, period=14):
    return DNA(SCHEMA, values={"flag": flag, "rsi.period": period})


class TestIndividualProtocol:

    def test_valid_implementation(self):
        class MyIndividual:
            def __init__(self, dna):
                self.dna = dna
                self.scores = {}

        ind = MyIndividual(_make_dna())
        assert isinstance(ind, Individual)

    def test_missing_dna_not_individual(self):
        class NoDna:
            def __init__(self):
                self.scores = {}

        assert not isinstance(NoDna(), Individual)

    def test_missing_scores_not_individual(self):
        class NoScores:
            def __init__(self, dna):
                self.dna = dna

        assert not isinstance(NoScores(_make_dna()), Individual)

    def test_scores_dict_usage(self):
        class MyIndividual:
            def __init__(self, dna):
                self.dna = dna
                self.scores = {}

        ind = MyIndividual(_make_dna())
        ind.scores["sharpe"] = 1.5
        ind.scores["mdd"] = -0.2
        assert ind.scores["sharpe"] == 1.5
        assert ind.scores["mdd"] == -0.2

    def test_dna_accessible(self):
        class MyIndividual:
            def __init__(self, dna):
                self.dna = dna
                self.scores = {}

        dna = _make_dna(True, 20)
        ind = MyIndividual(dna)
        assert ind.dna is dna
        assert ind.dna.get_path("rsi.period").value == 20
