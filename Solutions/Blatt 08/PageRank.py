from mrjob.job import MRJob


class MRPageRank(MRJob):
    def configure_args(self):
        self.add_passthru_arg('--beta', type=float, default=0.85)
        self.add_passthru_arg('-N', type=int)
        return super().configure_args()

    def mapper(self, _, line):
        """
        Reads a line of :math:`i, dest_1, \\dots, dest_{d_{i}}, r^old_i` and yields
        a portion of undamped pagerank for each destination.
        """
        fields = line.split()
        i, *dests = map(int, fields[:-1])
        r0_i = float(fields[-1])
        for dest in dests:
            yield dest, r0_i / len(dests)

    def reducer(self, k, v):
        """
        Weighted sum of contributions (incl. teleport) to each node's PageRank.
        """
        yield k, self.options.beta * sum(v) + (1 - self.options.beta) / self.options.N
