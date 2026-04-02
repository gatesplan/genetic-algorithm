# RandomSpawner

스키마 기반 완전 랜덤 DNA 생성. 교차/변이 없음.

## RandomSpawner

### __init__
__init__(schemas)
    schemas: GeneSchema | SequenceSchema 목록.

### Methods

spawn(population, culling_pool) -> DNA
    스키마 범위 내 랜덤 DNA 생성.
    population 무시. culling_pool에 있는 DNA는 재시도.
