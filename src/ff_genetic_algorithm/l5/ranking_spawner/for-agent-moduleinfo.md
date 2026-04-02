# RankingSpawner

score 항목별 랭크 기반 DNA 단건 생성. 지수감쇠 확률로 상위권 편중 선택, 서로 다른 score 분야에서 부모 선택 후 교차+변이.

## RankingSpawner

### __init__
__init__(schemas, score_names, decay=0.9, mutation_rate=0.005, alpha=0.5)
    schemas: GeneSchema | SequenceSchema 목록.
    score_names: 랭크 평가할 score 키 목록.
    decay: 지수감쇠 계수. 0에 가까울수록 상위 집중.
    mutation_rate: gene별 변이 확률.
    alpha: BLX-alpha 교차 계수.

### Methods

spawn(population, culling_pool) -> DNA
    score_names에서 2개 카테고리 선택, 각 랭킹에서 지수감쇠 확률로 부모 선택.
    crossover -> mutate. culling_pool에 있는 DNA는 재시도.
    DNA 1개 반환.
