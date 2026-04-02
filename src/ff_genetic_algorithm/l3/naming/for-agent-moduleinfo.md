# naming

DNA 비트열을 한글 완성형(가~힣)으로 인코딩/디코딩.
13bit 단위로 한 글자 매핑 (2^13=8192 < 11172). 비트 손실 없음.

## Functions

dna_to_name(dna) -> str
    DNA -> 한글 이름. 8글자씩 대시 구분.

bits_to_name(bits) -> str
    비트열 문자열 -> 한글 이름.

name_to_bits(name) -> str
    한글 이름 -> 비트열 복원.

name_to_short(name) -> str
    첫 그룹만 반환 (표시용).
