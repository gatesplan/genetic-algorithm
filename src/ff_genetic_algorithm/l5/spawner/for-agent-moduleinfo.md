# Spawner

Spawner Protocol. spawn(population, culling_pool) -> DNA 인터페이스 정의.

## Spawner (Protocol)

runtime_checkable. 구체 클래스는 import/상속 불필요.
spawn 메서드만 구현하면 자동 만족.

### Methods

spawn(population, culling_pool) -> DNA
    population에서 부모 선택, DNA 1개 생성 반환.
