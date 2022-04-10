from collections import Counter
from functools import reduce

import pytest

from pyhlips._counted_labels import Problem_A, Problem_B, create_labeling


def _count(x: Counter, y):
    x.update(y)
    return x


def test_problem_a():
    p = Problem_A([1, 2, 3], [3, 0, 1])
    x = p.get_a_solution()
    assert x[0] == [0, 0, 1]
    assert x[1] == [1, 0, 1]
    assert x[2] == [2, 0, 1]


def test_problem_b():

    s, k = 10, 3
    a = [9, 7, 10, 3, 1]

    p = Problem_B(10, 3, [9, 7, 10, 3, 1])
    solution = p.items
    for item in solution.values():
        assert len(item) == k  # item has k labels
        assert len(set(item)) == k  # none of them repeatedly
    counter = reduce(_count, solution.values(), Counter())
    for i in counter:
        assert counter[i] == a[i]


def test_create_labeling():
    labels = {"A": 3, "C": 1}
    s = [2, 1]
    items = create_labeling(labels, s)
    assert len(items) == 3
    counter = reduce(_count, items, Counter())
    for label in counter:
        assert counter[label] == labels[label]
    counter = Counter((len(labels) for labels in items))
    for k in counter:
        assert counter[k] == s[k - 1]
