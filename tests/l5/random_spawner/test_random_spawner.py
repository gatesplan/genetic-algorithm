import pytest
from ff_genetic_algorithm.l0.gene_schema import GeneSchema
from ff_genetic_algorithm.l2.dna import DNA
from ff_genetic_algorithm.l4.culling_pool import CullingPool
from ff_genetic_algorithm.l4.population import PopulationPool
from ff_genetic_algorithm.l5.random_spawner import RandomSpawner


SCHEMA = [
    GeneSchema("flag", bool),
    GeneSchema("count", int, range=(0, 100)),
    GeneSchema("ratio", float, range=(0.0, 1.0)),
]


class TestRandomSpawnerBasic:

    def test_spawn_returns_dna(self):
        spawner = RandomSpawner(SCHEMA)
        dna = spawner.spawn(PopulationPool(), CullingPool())
        assert isinstance(dna, DNA)

    def test_spawn_values_within_schema(self):
        spawner = RandomSpawner(SCHEMA)
        for _ in range(20):
            dna = spawner.spawn(PopulationPool(), CullingPool())
            vals = dna.to_values()
            assert vals["flag"] in (True, False)
            assert 0 <= vals["count"] <= 100
            assert 0.0 <= vals["ratio"] <= 1.0

    def test_spawn_ignores_population(self):
        spawner = RandomSpawner(SCHEMA)
        dna1 = spawner.spawn(PopulationPool(), CullingPool())
        dna2 = spawner.spawn(PopulationPool(), CullingPool())
        # random이니 다를 수 있지만, 둘 다 유효해야 함
        assert isinstance(dna1, DNA)
        assert isinstance(dna2, DNA)


class TestRandomSpawnerCulling:

    def test_avoids_culled_dna(self):
        spawner = RandomSpawner(SCHEMA)
        culling = CullingPool()
        dna = spawner.spawn(PopulationPool(), culling)
        assert not culling.seen(dna)


class TestRandomSpawnerVariety:

    def test_produces_different_dna(self):
        spawner = RandomSpawner(SCHEMA)
        culling = CullingPool()
        values_set = set()
        for _ in range(20):
            dna = spawner.spawn(PopulationPool(), culling)
            values_set.add(dna.to_int())
        assert len(values_set) > 1
