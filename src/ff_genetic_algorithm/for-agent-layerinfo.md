# for-agent-layerinfo.md

## l0
- GeneSchema, SequenceSchema

## l1
- gene: 단일 유전자 인스턴스, 비트 인코딩
- sequence: 유전자 그룹 컨테이너

## l2
- dna: 최상위 유전 데이터 컨테이너, 경로 접근, 마이그레이션
- dna_ops: DNA 유전 연산자 (crossover, mutate)

## l3
- dna_pool: DNA 중복 제거 컬렉션
- individual: 개체 Protocol (dna + scores)

## l4
- culling_pool: DNA 이력 추적 (seen/mark)
- spawning_pool: 랜덤 DNA 생성 팩토리
- population: 현재 세대 Individual 관리, 정렬/필터링

## l5
- spawner: Spawner Protocol
- population_filter: 구조적 결함 Individual 퍼지 제거
- elite_spawner: 순위합산 상위 DNA 복사
- tournament_spawner: 토너먼트 선택 교차+변이
- ranking_spawner: score별 랭크 지수감쇠 선택 교차+변이
- random_spawner: 스키마 기반 랜덤 DNA 생성
