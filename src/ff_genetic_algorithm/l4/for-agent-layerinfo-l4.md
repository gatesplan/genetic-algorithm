# l4

## culling_pool
CullingPool.__init__()
CullingPool.mark(dna) -> bool
CullingPool.seen(dna) -> bool

## spawning_pool
SpawningPool.__init__(schemas)
SpawningPool.spawn() -> DNA
SpawningPool.spawn_batch(n) -> list[DNA]
SpawningPool.contains(dna) -> bool
SpawningPool.clear() -> None

## score_ranking
rank_sum(individuals, score_names) -> dict[int, int]

## population
PopulationPool.__init__()
PopulationPool.add(individual) -> bool
PopulationPool.get(dna) -> Individual | None
PopulationPool.sort_by(score_name, reverse=True) -> list[Individual]
PopulationPool.filter_by(score_name, min_val=None, max_val=None) -> list[Individual]
PopulationPool.top(n, score_name) -> list[Individual]
PopulationPool.clear() -> None
