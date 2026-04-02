# score_ranking

Individual 컬렉션의 복수 score 기반 순위합산.

## Functions

rank_sum(individuals, score_names) -> dict[int, int]
    각 score_name별로 individuals를 내림차순 정렬, 순위 부여.
    모든 score의 순위를 합산. 반환값은 {id(ind): rank_sum}.
    값이 낮을수록 상위. score 없는 개체는 0으로 취급.
