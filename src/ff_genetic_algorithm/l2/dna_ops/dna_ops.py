import random

from ..dna import DNA


def crossover(dna_a, dna_b, schemas, alpha=0.5):
    genes_a = dna_a.flat()
    genes_b = dna_b.flat()
    values = {}
    flat_keys = _flat_keys(schemas)

    for key, ga, gb in zip(flat_keys, genes_a, genes_b):
        s = ga.schema
        if s.type is float:
            values[key] = _blx_alpha(ga.value, gb.value, s, alpha)
        else:
            values[key] = random.choice([ga.value, gb.value])

    return DNA(schemas, values=values)


def mutate(dna, schemas, rate=0.005):
    genes = dna.flat()
    flat_keys = _flat_keys(schemas)
    values = {}

    for key, gene in zip(flat_keys, genes):
        if random.random() < rate:
            values[key] = _random_gene_value(gene.schema)
        else:
            values[key] = gene.value

    return DNA(schemas, values=values)


def _blx_alpha(va, vb, schema, alpha):
    lo = min(va, vb)
    hi = max(va, vb)
    d = hi - lo
    low_bound = lo - alpha * d
    high_bound = hi + alpha * d
    if schema.range is not None:
        low_bound = max(low_bound, schema.range[0])
        high_bound = min(high_bound, schema.range[1])
    result = low_bound + random.random() * (high_bound - low_bound)
    return round(result, 3)


def _random_gene_value(schema):
    if schema.choices is not None:
        return random.choice(schema.choices)
    if schema.type is bool:
        return random.choice([True, False])
    if schema.type is int:
        return random.randint(schema.range[0], schema.range[1])
    if schema.type is float:
        val = schema.range[0] + random.random() * (schema.range[1] - schema.range[0])
        return round(val, 3)


def _flat_keys(schemas, prefix=""):
    keys = []
    for s in schemas:
        key = f"{prefix}{s.name}" if prefix else s.name
        if hasattr(s, 'children'):
            keys.extend(_flat_keys(s.children, key + "."))
        else:
            keys.append(key)
    return keys
