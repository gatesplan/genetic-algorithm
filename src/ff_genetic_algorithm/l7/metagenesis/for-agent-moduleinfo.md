# metagenesis

세대 교체 조율기. purge -> evolve -> next gen ready 사이클을 한 호출로 처리.

## Classes

Metagenesis.__init__(spawners, purge_rules)
    spawners: list of (Spawner, int) -- EvolutionPool 내부 생성.
    purge_rules: list of Callable[[list[Individual]], list[Individual]].
    spawner가 Spawner Protocol 불만족시 TypeError.

Metagenesis.next(population, culling_pool) -> tuple[PopulationPool, CullingPool]
    1. PopulationPurgeFilter.apply(population, culling_pool, purge_rules)
    2. EvolutionPool.evolve(purged_pop, culling_pool)
    새 PopulationPool의 Individual들은 scores가 비어있음.
    culling_pool은 동일 객체 (도태 + 신규 DNA 누적).
