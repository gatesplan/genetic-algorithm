import pytest
from ff_genetic_algorithm.l0.gene_schema import GeneSchema
from ff_genetic_algorithm.l0.sequence_schema import SequenceSchema
from ff_genetic_algorithm.l2.dna import DNA
from ff_genetic_algorithm.l4.spawning_pool import SpawningPool


SCHEMA = [
    GeneSchema("flag", bool),
    SequenceSchema("rsi", [
        GeneSchema("period", int, range=(5, 30)),
        GeneSchema("overbought", float, range=(60.0, 90.0)),
    ]),
]


class TestSpawningPoolSpawn:

    def test_spawn_returns_dna(self):
        pool = SpawningPool(SCHEMA)
        dna = pool.spawn()
        assert isinstance(dna, DNA)

    def test_spawn_random_values(self):
        pool = SpawningPool(SCHEMA)
        ints = set()
        for _ in range(50):
            dna = pool.spawn()
            ints.add(dna.to_int())
        assert len(ints) > 1

    def test_spawn_tracks_in_pool(self):
        pool = SpawningPool(SCHEMA)
        dna = pool.spawn()
        assert pool.contains(dna) is True

    def test_spawn_no_duplicates(self):
        pool = SpawningPool(SCHEMA)
        ints = set()
        for _ in range(100):
            dna = pool.spawn()
            assert dna.to_int() not in ints
            ints.add(dna.to_int())


class TestSpawningPoolSpawnBatch:

    def test_spawn_batch(self):
        pool = SpawningPool(SCHEMA)
        dnas = pool.spawn_batch(10)
        assert len(dnas) == 10
        ints = {d.to_int() for d in dnas}
        assert len(ints) == 10

    def test_spawn_batch_all_unique(self):
        pool = SpawningPool(SCHEMA)
        batch1 = pool.spawn_batch(5)
        batch2 = pool.spawn_batch(5)
        all_ints = {d.to_int() for d in batch1 + batch2}
        assert len(all_ints) == 10


class TestSpawningPoolSize:

    def test_size_after_spawn(self):
        pool = SpawningPool(SCHEMA)
        assert pool.size == 0
        pool.spawn()
        assert pool.size == 1
        pool.spawn_batch(5)
        assert pool.size == 6


class TestSpawningPoolClear:

    def test_clear(self):
        pool = SpawningPool(SCHEMA)
        pool.spawn_batch(5)
        pool.clear()
        assert pool.size == 0
