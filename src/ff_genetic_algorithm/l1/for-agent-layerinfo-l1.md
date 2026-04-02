# l1

## gene
Gene.__init__(schema, value=None)
Gene.bit_length() -> int
Gene.to_bits() -> str
Gene.from_bits(bit_str) -> None

## sequence
Sequence.__init__(name, children)
Sequence.get(name) -> Gene | Sequence | None
Sequence.flat() -> list[Gene]
