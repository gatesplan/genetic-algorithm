import pytest
from ff_genetic_algorithm.l0.gene_schema import GeneSchema
from ff_genetic_algorithm.l0.sequence_schema import SequenceSchema
from ff_genetic_algorithm.l2.dna import DNA
from ff_genetic_algorithm.l4.population import Population


SCHEMA = [
    GeneSchema("flag", bool),
    SequenceSchema("rsi", [
        GeneSchema("period", int, range=(5, 30)),
    ]),
]


def _make_dna(flag, period):
    return DNA(SCHEMA, values={"flag": flag, "rsi.period": period})


class TestPopulationAdd:

    def test_add(self):
        pop = Population()
        dna = _make_dna(True, 14)
        pop.add(dna)
        assert pop.size == 1

    def test_add_duplicate_rejected(self):
        pop = Population()
        dna1 = _make_dna(True, 14)
        dna2 = _make_dna(True, 14)
        assert pop.add(dna1) is True
        assert pop.add(dna2) is False
        assert pop.size == 1


class TestPopulationFitness:

    def test_set_and_get_fitness(self):
        pop = Population()
        dna = _make_dna(True, 14)
        pop.add(dna)
        pop.set_fitness(dna, 0.85)
        assert pop.get_fitness(dna) == 0.85

    def test_fitness_default_none(self):
        pop = Population()
        dna = _make_dna(True, 14)
        pop.add(dna)
        assert pop.get_fitness(dna) is None

    def test_set_fitness_multiple(self):
        pop = Population()
        dna1 = _make_dna(True, 14)
        dna2 = _make_dna(False, 20)
        pop.add(dna1)
        pop.add(dna2)
        pop.set_fitness(dna1, 0.9)
        pop.set_fitness(dna2, 0.3)
        assert pop.get_fitness(dna1) == 0.9
        assert pop.get_fitness(dna2) == 0.3


class TestPopulationRanking:

    def test_ranked_by_fitness_descending(self):
        pop = Population()
        dnas = [_make_dna(True, i) for i in range(5, 10)]
        fitnesses = [0.3, 0.9, 0.1, 0.7, 0.5]
        for dna, fit in zip(dnas, fitnesses):
            pop.add(dna)
            pop.set_fitness(dna, fit)
        ranked = pop.ranked()
        scores = [f for _, f in ranked]
        assert scores == sorted(scores, reverse=True)

    def test_ranked_returns_dna_fitness_pairs(self):
        pop = Population()
        dna = _make_dna(True, 14)
        pop.add(dna)
        pop.set_fitness(dna, 0.5)
        ranked = pop.ranked()
        assert len(ranked) == 1
        assert ranked[0] == (dna, 0.5)

    def test_ranked_excludes_none_fitness(self):
        pop = Population()
        dna1 = _make_dna(True, 14)
        dna2 = _make_dna(False, 20)
        pop.add(dna1)
        pop.add(dna2)
        pop.set_fitness(dna1, 0.5)
        ranked = pop.ranked()
        assert len(ranked) == 1


class TestPopulationSelect:

    def test_top_n(self):
        pop = Population()
        dnas = [_make_dna(True, i) for i in range(5, 15)]
        for i, dna in enumerate(dnas):
            pop.add(dna)
            pop.set_fitness(dna, float(i))
        top = pop.top(3)
        assert len(top) == 3
        fitnesses = [pop.get_fitness(d) for d in top]
        assert fitnesses == [9.0, 8.0, 7.0]

    def test_top_n_exceeds_size(self):
        pop = Population()
        dna = _make_dna(True, 14)
        pop.add(dna)
        pop.set_fitness(dna, 1.0)
        top = pop.top(5)
        assert len(top) == 1


class TestPopulationIterate:

    def test_iter_all(self):
        pop = Population()
        for i in range(5, 10):
            pop.add(_make_dna(True, i))
        assert len(list(pop)) == 5


class TestPopulationClear:

    def test_clear(self):
        pop = Population()
        pop.add(_make_dna(True, 14))
        pop.clear()
        assert pop.size == 0
