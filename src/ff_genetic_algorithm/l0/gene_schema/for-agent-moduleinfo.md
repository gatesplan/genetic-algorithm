# GeneSchema

단일 유전자 정의. 타입, 범위, 선택지를 지정하고 Gene 인스턴스를 생성하는 팩토리.

## GeneSchema

유전자의 구조를 정의. bool, int, float, enum(choices) 타입 지원.

### Properties
name: str                    # 유전자 이름
type: type | None            # bool, int, float (choices 사용 시 None)
range: tuple | None          # (min, max) int/float 전용
choices: list | None         # enum 선택지

### __init__
__init__(name, type=None, *, range=None, choices=None)
    raise ValueError
    choices 지정 시 type/range 무시.
    bool은 range 불필요.
    int/float은 range 필수, min < max.
    choices는 비어있으면 안됨.

### Methods

create(value=None) -> Gene
    Gene 인스턴스 생성.
    value 없으면 랜덤 초기화.
