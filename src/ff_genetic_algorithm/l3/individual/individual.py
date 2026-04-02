from typing import Protocol, runtime_checkable

from ...l2.dna import DNA


@runtime_checkable
class Individual(Protocol):

    dna: DNA
    scores: dict[str, float]
