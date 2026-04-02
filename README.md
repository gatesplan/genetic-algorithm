# ff-genetic-algorithm

Hierarchical gene structure based genetic algorithm framework for Python.

Schema-driven DNA representation with layered pool management,
multiple spawner strategies, and end-to-end generation cycle support.

## Installation

```bash
pip install ff-genetic-algorithm
```

Requires Python >= 3.10. No external dependencies.

## Usage

### DNA Schema Definition

```python
from ff_genetic_algorithm.l0.gene_schema import GeneSchema
from ff_genetic_algorithm.l0.sequence_schema import SequenceSchema

# -- Gene types --
# bool: True/False
GeneSchema("use_trailing", bool)

# int: range required (inclusive)
GeneSchema("leverage", int, range=(1, 10))

# float: range required, values rounded to 3 decimal places
GeneSchema("stop_loss", float, range=(0.01, 0.1))

# choices: enum-like selection from a list
GeneSchema("strategy", choices=["momentum", "mean_reversion", "breakout"])

# -- Sequence: groups genes into a named unit --
SequenceSchema("rsi", [
    GeneSchema("period", int, range=(5, 50)),
    GeneSchema("threshold", float, range=(20.0, 80.0)),
])

# -- Nested sequences --
SequenceSchema("indicators", [
    SequenceSchema("rsi", [
        GeneSchema("period", int, range=(5, 50)),
        GeneSchema("threshold", float, range=(20.0, 80.0)),
    ]),
    SequenceSchema("macd", [
        GeneSchema("fast", int, range=(5, 20)),
        GeneSchema("slow", int, range=(20, 50)),
    ]),
])

# -- Full schema list --
schemas = [
    GeneSchema("leverage", int, range=(1, 10)),
    GeneSchema("stop_loss", float, range=(0.01, 0.1)),
    GeneSchema("use_trailing", bool),
    GeneSchema("strategy", choices=["momentum", "mean_reversion", "breakout"]),
    SequenceSchema("rsi", [
        GeneSchema("period", int, range=(5, 50)),
        GeneSchema("threshold", float, range=(20.0, 80.0)),
    ]),
]

# -- DNA access --
from ff_genetic_algorithm.l2.dna import DNA

dna = DNA(schemas)                              # random init
dna = DNA(schemas, values={"leverage": 5})      # partial values, rest random

dna.get("leverage").value                       # -> 5
dna.get_path("rsi.period").value                # -> nested access
dna.to_values()                                 # -> {"leverage": 5, "rsi.period": 30, ...}

# -- Hangul naming --
# DNA bit-strings are encoded into Hangul syllables (0xAC00~0xD7A3).
# Each character encodes 13 bits (2^13 = 8,192 < 11,172 syllables),
# providing lossless compression with high information density per character.
from ff_genetic_algorithm.l3.naming import dna_to_name, name_to_bits, name_to_short

name = dna_to_name(dna)                         # -> "갈힣뮤텨퍅곣릐봤"
short = name_to_short(name)                     # -> first 8-char group
bits = name_to_bits(name)                       # -> lossless bit-string restoration
```

### Individual Implementation

Individual is a Protocol -- any object with `dna` and `scores` attributes satisfies it.

```python
from ff_genetic_algorithm.l2.dna import DNA

class Trader:
    def __init__(self, dna):
        self.dna = dna
        self.scores = {}

    def grow(self):
        """Domain-specific evaluation. Fill scores after simulation."""
        leverage = self.dna.get("leverage").value
        period = self.dna.get_path("rsi.period").value
        # ... run trading simulation ...
        self.scores["sharpe"] = 1.5
        self.scores["mdd"] = -0.12
```

### Metagenesis (Generation Cycle)

```python
from ff_genetic_algorithm.l4.culling_pool import CullingPool
from ff_genetic_algorithm.l4.population import PopulationPool
from ff_genetic_algorithm.l4.spawning_pool import SpawningPool
from ff_genetic_algorithm.l5.elite_spawner import EliteSpawner
from ff_genetic_algorithm.l5.tournament_spawner import TournamentSpawner
from ff_genetic_algorithm.l5.ranking_spawner import RankingSpawner
from ff_genetic_algorithm.l5.random_spawner import RandomSpawner
from ff_genetic_algorithm.l7.metagenesis import Metagenesis

# -- Initial population --
spawning = SpawningPool(schemas)
culling = CullingPool()
population = PopulationPool()

for dna in spawning.spawn_batch(512):
    population.add(Trader(dna))
    culling.mark(dna)

# -- Purge rules --
def top_half(individuals):
    ranked = sorted(individuals, key=lambda i: i.scores.get("sharpe", 0), reverse=True)
    return ranked[:len(ranked) // 2]

# -- Metagenesis setup --
score_names = ["sharpe", "mdd"]

meta = Metagenesis(
    spawners=[
        (EliteSpawner(schemas, score_names), 128),
        (TournamentSpawner(schemas, k=5, score_names=score_names), 128),
        (RankingSpawner(schemas, score_names), 128),
        (RandomSpawner(schemas), 128),
    ],
    purge_rules=[top_half],
)

# -- Generation loop --
for gen in range(100):
    # Grow: domain fills scores
    for ind in population:
        ind.grow()

    # Next generation
    population, culling = meta.next(population, culling)
```

## Reference

### l0

```
gene_schema
    GeneSchema.__init__(name, type=None, *, range=None, choices=None)
    GeneSchema.create(value=None) -> Gene

sequence_schema
    SequenceSchema.__init__(name, children)
    SequenceSchema.create(values=None) -> Sequence
```

### l1

```
gene
    Gene.__init__(schema, value=None)
    Gene.bit_length() -> int
    Gene.to_bits() -> str
    Gene.from_bits(bit_str) -> None

sequence
    Sequence.__init__(name, children)
    Sequence.get(name) -> Gene | Sequence | None
    Sequence.flat() -> list[Gene]
```

### l2

```
dna
    DNA.__init__(schemas, values=None)
    DNA.get(name) -> Gene | Sequence | None
    DNA.get_path(path) -> Gene | Sequence | None
    DNA.flat() -> list[Gene]
    DNA.to_bits() -> str
    DNA.to_int() -> int
    DNA.from_bits(bit_str) -> None
    DNA.to_values() -> dict[str, any]

dna_ops
    crossover(dna_a, dna_b, schemas, alpha=0.5) -> DNA
    mutate(dna, schemas, rate=0.005) -> DNA
```

### l3

```
dna_pool
    DnaPool.__init__()
    DnaPool.add(dna) -> bool
    DnaPool.contains(dna) -> bool
    DnaPool.remove(dna) -> bool

individual
    Individual (Protocol)
    Individual.dna: DNA
    Individual.scores: dict[str, float]

naming
    dna_to_name(dna) -> str
    bits_to_name(bits) -> str
    name_to_bits(name) -> str
    name_to_short(name) -> str
```

### l4

```
culling_pool
    CullingPool.__init__()
    CullingPool.mark(dna) -> bool
    CullingPool.seen(dna) -> bool

spawning_pool
    SpawningPool.__init__(schemas)
    SpawningPool.spawn() -> DNA
    SpawningPool.spawn_batch(n) -> list[DNA]
    SpawningPool.contains(dna) -> bool
    SpawningPool.clear() -> None

score_ranking
    rank_sum(individuals, score_names) -> dict[int, int]

population
    PopulationPool.__init__()
    PopulationPool.add(individual) -> bool
    PopulationPool.get(dna) -> Individual | None
    PopulationPool.sort_by(score_name, reverse=True) -> list[Individual]
    PopulationPool.filter_by(score_name, min_val=None, max_val=None) -> list[Individual]
    PopulationPool.top(n, score_name) -> list[Individual]
    PopulationPool.clear() -> None
```

### l5

```
spawner
    Spawner (Protocol)
    Spawner.spawn(population, culling_pool) -> DNA

population_filter
    PopulationPurgeFilter.__init__()
    PopulationPurgeFilter.apply(population, culling_pool, rules)
        -> tuple[PopulationPool, CullingPool]

elite_spawner
    EliteSpawner.__init__(schemas, score_names)
    EliteSpawner.spawn(population, culling_pool) -> DNA

tournament_spawner
    TournamentSpawner.__init__(schemas, k, score_names,
        mutation_rate=0.005, alpha=0.5)
    TournamentSpawner.spawn(population, culling_pool) -> DNA

ranking_spawner
    RankingSpawner.__init__(schemas, score_names,
        decay=0.9, mutation_rate=0.005, alpha=0.5)
    RankingSpawner.spawn(population, culling_pool) -> DNA

random_spawner
    RandomSpawner.__init__(schemas)
    RandomSpawner.spawn(population, culling_pool) -> DNA
```

### l6

```
evolution_pool
    EvolutionPool.__init__(spawners)
    EvolutionPool.evolve(population, culling_pool)
        -> tuple[PopulationPool, CullingPool]
```

### l7

```
metagenesis
    Metagenesis.__init__(spawners, purge_rules)
    Metagenesis.next(population, culling_pool)
        -> tuple[PopulationPool, CullingPool]
```
