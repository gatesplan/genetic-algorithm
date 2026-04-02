# PopulationPurgeFilter

구조적 결함 Individual을 하드하게 제거하는 퍼지 필터.

## PopulationPurgeFilter

PopulationPool에서 규칙에 따라 부적격 Individual을 제거하고,
도태된 DNA를 CullingPool에 기록. 상태 없음(stateless).

### __init__
__init__()
    상태 없는 인스턴스 생성.

### Methods

apply(population, culling_pool, rules) -> tuple[PopulationPool, CullingPool]
    population의 Individual에 rules를 순차 적용.
    rules는 Callable[[list], list] 목록 (람다/함수).
    도태된 Individual의 DNA를 culling_pool에 mark.
    (새 PopulationPool, culling_pool) 튜플 반환.
