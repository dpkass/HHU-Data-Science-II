from itertools import combinations, chain
from collections import defaultdict

import numpy as np
from mrjob.job import MRJob


class LSH:
    def __init__(self, r):
        self.r = r

    def create_buckets(self, minhash_signatures):
        buckets = defaultdict(list)

        for doc_idx, signature in minhash_signatures.items():
            for band_start_idx in range(0, len(signature), self.r):
                band = signature[band_start_idx:min((band_start_idx + self.r), len(signature) - 1)]
                band_hash = hash_band(band)
                buckets[band_hash].append(doc_idx)

        return buckets

    def __call__(self, minhash_signatures):
        buckets = self.create_buckets(minhash_signatures)
        candidate_pairs = [list(combinations(idxs, 2)) for idxs in buckets.values()]
        return buckets, set(chain.from_iterable(candidate_pairs))


class MRLSH(MRJob):
    b = 20

    def mapper(self, _, line):
        id, *bands = line.split()
        for band in np.array_split(bands, MRLSH.b):
            yield hash_band(band), id

    def reducer(self, key, values):
        values = list(values)
        if len(values) > 1: yield key, '\t'.join(values)


def hash_band(band):
    return hash(tuple(band))
