# l2

## dna
DNA.__init__(schemas, values=None)
DNA.get(name) -> Gene | Sequence | None
DNA.get_path(path) -> Gene | Sequence | None
DNA.flat() -> list[Gene]
DNA.to_bits() -> str
DNA.to_int() -> int
DNA.from_bits(bit_str) -> None
DNA.to_values() -> dict[str, any]

## dna_ops
crossover(dna_a, dna_b, schemas, alpha=0.5) -> DNA
mutate(dna, schemas, rate=0.005) -> DNA
