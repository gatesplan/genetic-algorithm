import pytest
from ff_genetic_algorithm.l2.dna import DNA
from ff_genetic_algorithm.l5.spawner import Spawner


class ValidSpawner:
    def spawn(self, population, culling_pool):
        return DNA([], values={})


class MissingSpawn:
    pass


class WrongSignature:
    def spawn(self):
        pass


class TestSpawnerProtocol:

    def test_valid_spawner(self):
        assert isinstance(ValidSpawner(), Spawner)

    def test_missing_spawn_not_spawner(self):
        assert not isinstance(MissingSpawn(), Spawner)

    def test_tournament_spawner_is_spawner(self):
        from ff_genetic_algorithm.l5.tournament_spawner import TournamentSpawner
        from ff_genetic_algorithm.l0.gene_schema import GeneSchema
        schema = [GeneSchema("x", int, range=(0, 10))]
        spawner = TournamentSpawner(schema, k=2, score_names=["s"])
        assert isinstance(spawner, Spawner)

    def test_ranking_spawner_is_spawner(self):
        from ff_genetic_algorithm.l5.ranking_spawner import RankingSpawner
        from ff_genetic_algorithm.l0.gene_schema import GeneSchema
        schema = [GeneSchema("x", int, range=(0, 10))]
        spawner = RankingSpawner(schema, score_names=["s"])
        assert isinstance(spawner, Spawner)

    def test_elite_spawner_is_spawner(self):
        from ff_genetic_algorithm.l5.elite_spawner import EliteSpawner
        from ff_genetic_algorithm.l0.gene_schema import GeneSchema
        schema = [GeneSchema("x", int, range=(0, 10))]
        spawner = EliteSpawner(schema, score_names=["s"])
        assert isinstance(spawner, Spawner)

    def test_random_spawner_is_spawner(self):
        from ff_genetic_algorithm.l5.random_spawner import RandomSpawner
        from ff_genetic_algorithm.l0.gene_schema import GeneSchema
        schema = [GeneSchema("x", int, range=(0, 10))]
        spawner = RandomSpawner(schema)
        assert isinstance(spawner, Spawner)
