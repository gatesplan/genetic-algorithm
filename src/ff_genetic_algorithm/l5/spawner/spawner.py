from typing import Protocol, runtime_checkable

from ...l2.dna import DNA


@runtime_checkable
class Spawner(Protocol):

    def spawn(self, population, culling_pool) -> DNA: ...
