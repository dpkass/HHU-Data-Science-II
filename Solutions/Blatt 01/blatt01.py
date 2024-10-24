import sys

from mrjob.job import MRJob, MRStep


class MRSparseMatMul(MRJob):
    def steps(self):
        return [
            MRStep(mapper=self.cell_mapper, reducer=self.cell_reducer),
            MRStep(reducer=self.sum_reducer)
        ]

    def cell_mapper(self, _, line):
        mat, o, p, value = line.split()
        if mat == 'N': o, p = p, o  # o, p was j, k. we want key j

        yield p, (mat, o, float(value))

    def cell_reducer(self, _, values):
        M, N = [], []
        for (mat, i, v) in values: (M if mat == 'M' else N).append((i, v))

        for i, v1 in M:
            for k, v2 in N:
                yield (i, k), v1 * v2

    def sum_reducer(self, key, values):
        yield key, sum(values)


def run(input_file):
    job = MRSparseMatMul(args=[input_file])
    with job.make_runner() as runner:
        runner.run()
        return list(job.parse_output(runner.cat_output()))


if __name__ == '__main__':
    res = run(sys.argv[1])
    with open(sys.argv[2], 'w') as f:
        for (i, k), v in res: print(f"{i}\t{k}\t{str(v)}", file=f)
