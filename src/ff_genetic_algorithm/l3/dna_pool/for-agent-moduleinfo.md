# DnaPool

DNA 중복 제거 컬렉션. to_int() 기반 set 인덱스로 O(1) 중복 검사.

## DnaPool

CullingPool, SpawningPool, PopulationPool의 내부 저장소로 사용.

### Properties
size: int                    # 보유 DNA 수

### __init__
__init__()
    빈 풀 생성.

### Methods

add(dna) -> bool
    DNA 추가. 중복이면 False 반환.

contains(dna) -> bool
    DNA 존재 여부 확인.

remove(dna) -> bool
    DNA 제거. 없으면 False 반환.
