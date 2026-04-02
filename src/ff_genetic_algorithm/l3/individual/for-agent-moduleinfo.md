# Individual

개체 Protocol. 도메인에서 구체 클래스로 구현.

## Individual (Protocol, runtime_checkable)

GA 엔진이 관리하는 개체의 인터페이스.
dna와 scores 속성을 가진 아무 객체가 Individual을 만족.

### Properties
dna: DNA                     # 유전 데이터
scores: dict[str, float]     # 도메인별 성능 지표 (sharpe, mdd 등)
