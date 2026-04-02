# SpawningPool

랜덤 DNA 생성 팩토리. 내부 중복 방지.

## SpawningPool

스키마 기반으로 고유한 DNA를 생성. 내부 DnaPool로 중복 추적.

### Properties
size: int                    # 생성된 DNA 수

### __init__
__init__(schemas)
    schemas는 GeneSchema | SequenceSchema 목록.

### Methods

spawn() -> DNA
    고유한 DNA 1개 랜덤 생성.
    중복 시 내부 재시도.

spawn_batch(n) -> list[DNA]
    고유한 DNA n개 생성.

contains(dna) -> bool
    해당 DNA가 이 풀에서 생성되었는지 확인.

clear() -> None
    내부 추적 초기화.
