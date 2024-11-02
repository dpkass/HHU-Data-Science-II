import numpy as np
from itertools import chain


class KShingles:
    def __init__(self, k):
        assert k > 0
        self.k = k

    def __call__(self, entry):
        for i in range(len(entry) - self.k + 1):
            yield entry[i:i + self.k]


class HashFunction:
    def __init__(self, a, b, p, n): self.a, self.b, self.p, self.n = a, b, p, n

    def __call__(self, x): return (self.a * x + self.b) % self.p % self.n


class MinHash:
    def __init__(self, k):
        self.k_shingles = KShingles(k)
        self.minhash = lambda n: (lambda x: minhash_vector(x, create_hashfunctions(n)))

    def __call__(self, entries):
        """
        :param entries: pd.Series or pd.DataFrame
        """
        documents = entries.map(self.k_shingles).map(set)
        shingle_index_map = create_shingles_index(documents)
        return documents.map(self.minhash(len(shingle_index_map)))


def create_shingles_index(shingles_column):
    all_shingles = list(chain.from_iterable(shingles_column))
    unique_shingles = sorted(set(all_shingles))
    shingle_index_map = {shingle: i for i, shingle in enumerate(unique_shingles)}

    return shingle_index_map


def shingle_vector(shingle_index_map, shingle_set):
    vec = np.zeros(len(shingle_index_map), dtype=bool)
    for shingle in shingle_set: vec[shingle_index_map[shingle]] = True

    return vec


def _next_prime(n):
    is_prime = lambda n: all(n % i for i in range(2, int(n ** 0.5) + 1))
    while not is_prime(n): n += 1
    return n


def create_hashfunctions(n, H=100):
    p = _next_prime(n)

    all_a = np.random.randint(1, n, H)
    all_b = np.random.randint(0, n, H)

    return np.array([
        HashFunction(a, b, p, n)
        for a, b in zip(all_a, all_b)
    ])


def minhash_vector(shingle_vector, hs):
    minhashes = np.full(len(hs), np.inf)

    for shingle_i, present in enumerate(shingle_vector):
        if not present: continue
        for i, h in enumerate(hs):
            minhashes[i] = min(minhashes[i], h(shingle_i))

    return minhashes
