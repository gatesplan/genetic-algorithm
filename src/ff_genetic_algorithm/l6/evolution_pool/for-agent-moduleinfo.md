# evolution_pool

Spawner 조합으로 새 세대를 생성하는 진화 조율기.

## Classes

EvolutionPool.__init__(spawners)
    spawners: list of (Spawner, int) -- (spawner instance, target count).
    각 spawner가 Spawner Protocol을 만족하는지 isinstance 검증.
    불만족시 TypeError.

EvolutionPool.evolve(population, culling_pool) -> tuple[PopulationPool, CullingPool]
    각 (spawner, count) 쌍에 대해 spawner.spawn()을 count회 호출.
    반환된 DNA를 culling_pool.mark() 후 Individual로 감싸 새 PopulationPool에 추가.
    새 Individual의 scores는 비어있음.
    culling_pool은 동일 객체 (누적).
