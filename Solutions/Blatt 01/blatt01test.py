import unittest
from blatt01 import run


class TestMRMatrixMatrixMul(unittest.TestCase):
    def check(self, input_file, expected_file):
        actual = set((i, k, v) for (i, k), v in run(input_file))
        with open(expected_file, 'r') as f:
            lines = [line.strip().split() for line in f.readlines()]
            expected = set((i, k, float(v)) for i, k, v in lines)
        self.assertSetEqual(actual, expected)

    def test(self):
        num_cases = 5
        ins = [f'test_cases/in{i:02}' for i in range(1, num_cases + 1)]
        outs = [f'test_cases/out{i:02}' for i in range(1, num_cases + 1)]

        for in_, out in zip(ins, outs): self.check(in_, out)
