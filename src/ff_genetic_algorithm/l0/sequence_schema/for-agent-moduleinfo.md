# SequenceSchema

유전자 그룹 정의. GeneSchema/SequenceSchema를 자식으로 가지며 재귀 중첩 가능.

## SequenceSchema

복합 유전자 구조 정의. Sequence 인스턴스를 생성하는 팩토리.

### Properties
name: str                    # 시퀀스 이름
children: list               # GeneSchema | SequenceSchema 목록

### __init__
__init__(name, children)
    raise ValueError
    raise TypeError
    children 비어있으면 안됨.
    children은 GeneSchema 또는 SequenceSchema만 허용.

### Methods

create(values=None) -> Sequence
    Sequence 인스턴스 생성.
    values는 자식 이름을 키로 하는 dict.
