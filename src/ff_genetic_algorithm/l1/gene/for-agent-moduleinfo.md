# Gene

단일 유전자 인스턴스. 값 보유, 비트 인코딩/디코딩 담당.

## Gene

GeneSchema로부터 생성. 타입별 비트 변환 로직 내장.

### Properties
schema: GeneSchema           # 원본 스키마 참조
name: str                    # schema.name 위임
value: any                   # 현재 유전자 값

### __init__
__init__(schema, value=None)
    value 없으면 타입별 랜덤 초기화.
    float은 소수점 3자리로 coerce.

### Methods

bit_length() -> int
    이 유전자의 비트 표현 길이.
    ceil(log2(steps)) 계산.

to_bits() -> str
    현재 값을 비트 문자열로 인코딩.
    float은 범위 내 클램핑 적용.

from_bits(bit_str) -> None
    비트 문자열에서 값 복원.
    비트 범위 > 값 범위일 때 max로 클램핑.
    교잡/돌연변이 후 안전한 디코딩 보장.
