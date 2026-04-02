# TournamentSpawner

토너먼트 선택 기반 DNA 단건 생성. k개 랜덤 뽑기에서 rank_sum 최상위 개체를 부모로 선택, 교차+변이.

## TournamentSpawner

### __init__
__init__(schemas, k, score_names, mutation_rate=0.005, alpha=0.5)
    schemas: GeneSchema | SequenceSchema 목록.
    k: 토너먼트 그룹 크기.
    score_names: 순위합산 대상 score 키 리스트.
    mutation_rate: gene별 변이 확률.
    alpha: BLX-alpha 교차 계수.

### Methods

spawn(population, culling_pool) -> DNA
    토너먼트 선택으로 부모 2명 -> crossover -> mutate.
    DNA 1개 반환.
