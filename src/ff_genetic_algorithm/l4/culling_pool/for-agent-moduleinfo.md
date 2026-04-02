# CullingPool

DNA 이력 추적 풀. 한번 도태된 DNA가 재등장하지 않도록 기록.

## CullingPool

DnaPool을 감싸서 mark/seen 인터페이스 제공. 누적 전용, 제거 없음.

### Properties
size: int                    # 기록된 DNA 수

### __init__
__init__()
    빈 풀 생성.

### Methods

mark(dna) -> bool
    DNA를 도태 기록에 추가. 이미 있으면 False.

seen(dna) -> bool
    DNA가 도태 기록에 있는지 확인.
