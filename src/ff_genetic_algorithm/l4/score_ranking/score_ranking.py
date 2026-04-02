def rank_sum(individuals, score_names):
    totals = {id(ind): 0 for ind in individuals}
    for name in score_names:
        ranked = sorted(individuals, key=lambda i: i.scores.get(name, 0), reverse=True)
        for rank, ind in enumerate(ranked):
            totals[id(ind)] += rank
    return totals
