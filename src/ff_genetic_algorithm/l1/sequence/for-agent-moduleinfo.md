# Sequence

유전자 그룹 컨테이너. Gene/Sequence를 자식으로 보유.

## Sequence

이름 기반 접근과 평탄화(flat) 지원.

### Properties
name: str                    # 시퀀스 이름
children: list               # Gene | Sequence 목록

### __init__
__init__(name, children)
    자식 목록 복사 저장.

### Methods

get(name) -> Gene | Sequence | None
    이름으로 직계 자식 검색.

flat() -> list[Gene]
    모든 하위 Gene을 재귀적으로 평탄화.
    Sequence는 풀어서 Gene만 반환.
