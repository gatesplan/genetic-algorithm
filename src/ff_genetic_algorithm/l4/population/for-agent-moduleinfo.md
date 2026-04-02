# PopulationPool

현재 세대 Individual 관리. 정렬, 필터링, 조회 담당.

## PopulationPool

Individual을 DNA 기준 중복 제거하며 보관. scores 기반 조회 기능 제공.

### Properties
size: int                    # 보유 Individual 수

### __init__
__init__()
    빈 풀 생성.

### Methods

add(individual) -> bool
    Individual 추가. DNA 중복이면 False.

get(dna) -> Individual | None
    DNA로 Individual 조회.

sort_by(score_name, reverse=True) -> list[Individual]
    특정 score 기준 정렬.
    해당 score 없는 Individual은 제외.

filter_by(score_name, min_val=None, max_val=None) -> list[Individual]
    score 임계값 필터링.
    해당 score 없는 Individual은 제외.

top(n, score_name) -> list[Individual]
    특정 score 상위 N개 반환.

clear() -> None
    전체 초기화.
