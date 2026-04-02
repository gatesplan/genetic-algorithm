# dna_ops

DNA 수준 유전 연산자. 교차(crossover)와 변이(mutate).

## Functions

crossover(dna_a, dna_b, schemas, alpha=0.5) -> DNA
    두 부모 DNA를 교차하여 새 DNA 생성.
    float 유전자: BLX-alpha (범위 확장 블렌드). alpha=0이면 부모 사이만.
    int/bool/choices 유전자: 부모 중 랜덤 택1.
    schema range로 clamp.

mutate(dna, schemas, rate=0.005) -> DNA
    gene별 rate 확률로 schema 범위 내 재랜덤.
    원본 불변, 새 DNA 반환.
