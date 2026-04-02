# DNA

최상위 유전 데이터 컨테이너. 스키마 목록으로 생성, 경로 접근, 비트 변환, 마이그레이션 지원.

## DNA

Gene/Sequence를 children으로 보유. 풀(pool)의 관리 단위.

### Properties
children: list               # Gene | Sequence 최상위 목록

### __init__
__init__(schemas, values=None)
    raise TypeError
    schemas는 GeneSchema | SequenceSchema 목록.
    values는 "path.key": value 형식 dict.
    values에 없는 유전자는 랜덤 초기화.

### Methods

get(name) -> Gene | Sequence | None
    최상위 자식 이름 검색.

get_path(path) -> Gene | Sequence | None
    점(.) 구분 경로로 중첩 접근.
    "rsi.period" -> rsi 시퀀스의 period 유전자.

flat() -> list[Gene]
    모든 Gene을 재귀적으로 평탄화.

to_bits() -> str
    전체 유전자 비트 연결.
    flat() 순서대로 각 Gene.to_bits() 연결.

to_int() -> int
    to_bits()를 정수로 변환.
    풀 중복 제거 키로 사용.

from_bits(bit_str) -> None
    비트 문자열에서 전체 유전자 값 복원.

to_values() -> dict[str, any]
    모든 유전자를 "path.key": value dict로 추출.
    마이그레이션 시 구 DNA에서 값 추출 용도.
