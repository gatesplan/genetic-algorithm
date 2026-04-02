# EliteSpawner

순위합산 기반 상위 개체 DNA 복사. 교차/변이 없음.

## EliteSpawner

상태 보유. population이 바뀌면 내부 순위 리셋.

### __init__
__init__(schemas, score_names)
    schemas: GeneSchema | SequenceSchema 목록.
    score_names: 순위합산에 사용할 score 키 목록.

### Methods

spawn(population, culling_pool) -> DNA
    순위합산 기준 상위부터 순서대로 DNA 복사 반환.
    호출마다 다음 순위. population 변경 시 리셋.
