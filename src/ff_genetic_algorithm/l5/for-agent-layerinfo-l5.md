# l5

## spawner
Spawner (Protocol)
Spawner.spawn(population, culling_pool) -> DNA

## population_filter
PopulationPurgeFilter.__init__()
PopulationPurgeFilter.apply(population, culling_pool, rules) -> tuple[PopulationPool, CullingPool]

## elite_spawner
EliteSpawner.__init__(schemas, score_names)
EliteSpawner.spawn(population, culling_pool) -> DNA

## tournament_spawner
TournamentSpawner.__init__(schemas, k, score_names, mutation_rate=0.005, alpha=0.5)
TournamentSpawner.spawn(population, culling_pool) -> DNA

## ranking_spawner
RankingSpawner.__init__(schemas, score_names, decay=0.9, mutation_rate=0.005, alpha=0.5)
RankingSpawner.spawn(population, culling_pool) -> DNA

## random_spawner
RandomSpawner.__init__(schemas)
RandomSpawner.spawn(population, culling_pool) -> DNA
