from mrjob.job import MRJob


class MR4Shingles(MRJob):
    def mapper(self, _, line):
        for i in range(len(line) - 4 + 1):
            yield line[i:i + 4], 1

    def reducer(self, key, values):
        yield key, sum(values)
