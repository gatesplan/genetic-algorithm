import pytest
from ff_genetic_algorithm.l4.score_ranking import rank_sum


class FakeInd:
    def __init__(self, **scores):
        self.scores = dict(scores)


class TestRankSumSingleScore:

    def test_single_score_ranking(self):
        inds = [FakeInd(sharpe=3.0), FakeInd(sharpe=1.0), FakeInd(sharpe=2.0)]
        result = rank_sum(inds, ["sharpe"])
        # sharpe: 3.0->rank0, 2.0->rank1, 1.0->rank2
        assert result[id(inds[0])] == 0
        assert result[id(inds[1])] == 2
        assert result[id(inds[2])] == 1

    def test_lower_rank_sum_is_better(self):
        inds = [FakeInd(sharpe=10.0), FakeInd(sharpe=1.0)]
        result = rank_sum(inds, ["sharpe"])
        assert result[id(inds[0])] < result[id(inds[1])]


class TestRankSumMultiScore:

    def test_two_scores(self):
        inds = [
            FakeInd(sharpe=3.0, winrate=1.0),  # sharpe rank0 + winrate rank2 = 2
            FakeInd(sharpe=1.0, winrate=3.0),  # sharpe rank2 + winrate rank0 = 2
            FakeInd(sharpe=2.0, winrate=2.0),  # sharpe rank1 + winrate rank1 = 2
        ]
        result = rank_sum(inds, ["sharpe", "winrate"])
        assert result[id(inds[0])] == 2
        assert result[id(inds[1])] == 2
        assert result[id(inds[2])] == 2

    def test_dominant_individual(self):
        inds = [
            FakeInd(sharpe=10.0, winrate=10.0),  # rank0 + rank0 = 0
            FakeInd(sharpe=1.0, winrate=1.0),    # rank1 + rank1 = 2
        ]
        result = rank_sum(inds, ["sharpe", "winrate"])
        assert result[id(inds[0])] == 0
        assert result[id(inds[1])] == 2

    def test_three_scores(self):
        inds = [
            FakeInd(a=3.0, b=1.0, c=2.0),  # ranks: 0+2+1 = 3
            FakeInd(a=1.0, b=3.0, c=3.0),  # ranks: 2+0+0 = 2
            FakeInd(a=2.0, b=2.0, c=1.0),  # ranks: 1+1+2 = 4
        ]
        result = rank_sum(inds, ["a", "b", "c"])
        assert result[id(inds[0])] == 3
        assert result[id(inds[1])] == 2
        assert result[id(inds[2])] == 4


class TestRankSumEdgeCases:

    def test_missing_score_treated_as_zero(self):
        inds = [FakeInd(sharpe=5.0), FakeInd()]
        result = rank_sum(inds, ["sharpe"])
        assert result[id(inds[0])] < result[id(inds[1])]

    def test_single_individual(self):
        inds = [FakeInd(sharpe=1.0)]
        result = rank_sum(inds, ["sharpe"])
        assert result[id(inds[0])] == 0

    def test_empty_score_names(self):
        inds = [FakeInd(sharpe=1.0), FakeInd(sharpe=2.0)]
        result = rank_sum(inds, [])
        assert result[id(inds[0])] == 0
        assert result[id(inds[1])] == 0
