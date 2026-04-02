# l3

## dna_pool
DnaPool.__init__()
DnaPool.add(dna) -> bool
DnaPool.contains(dna) -> bool
DnaPool.remove(dna) -> bool

## individual
Individual (Protocol)
Individual.dna: DNA
Individual.scores: dict[str, float]

## naming
dna_to_name(dna) -> str
bits_to_name(bits) -> str
name_to_bits(name) -> str
name_to_short(name) -> str
