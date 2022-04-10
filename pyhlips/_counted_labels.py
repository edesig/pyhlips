import random
from functools import cached_property
from typing import Dict, List

from cvxopt import matrix, spmatrix
from cvxopt.glpk import ilp


def projection(n):
    return lambda x: x[n]


class Problem_A:
    """
    Produces a_ij, where A_1, ..., A_n is a system of sets,
    that satisfies A_n has a_n elements, and the number of
    elements contained by exactly k of A_i-s is s_k, and where
    a_kj is the number of elements in A_k contained by exactly
    j A_i.
    """

    def __init__(self, a, s):
        """
        a = (a0, a1, a2, ... )
        s = (s1 (!), s2, s3, ...)
        """
        self.n = len(a)
        if self.n != len(s):
            raise AttributeError("|a| != |s|")
        self.a = a
        self.s = s

    @cached_property
    def _A(self: int):
        """
        returns a sparse matrix
        """
        # x_(i*n)+j = x_ij = | A_i && S_j |
        # s_j = `s[j-1]` = | S_j |
        n = self.n

        # x_i1 + x_i2 + ... + x_in = a_i (i=1, ..., n)
        A = [(1, y, y * n + x) for y in range(n) for x in range(n)]

        # x_1j + x_2j + ... + x_nj = j * s_j
        A += [(1, y + n, x * n + y) for y in range(n) for x in range(n)]

        return spmatrix(
            list(map(projection(0), A)),
            list(map(projection(1), A)),
            list(map(projection(2), A)),
        )

    @cached_property
    def _b(self):
        return matrix(
            tuple(
                list(self.a)
                + [(i_ + 1) * s_i for i_, s_i in enumerate(self.s)]
            ),  # i_ = i-1
            tc="d",
        )

    @cached_property
    def _G(self):
        d = self.n ** 2
        return spmatrix(
            tuple([1] * d + [-1] * d),
            tuple(range(2 * d)),
            tuple((y % d for y in range(2 * d))),
        )

    @cached_property
    def _h(self):
        d = self.n ** 2
        return matrix(
            tuple(tuple([s_i for s_i in self.s] * self.n) + (0,) * d), tc="d"
        )

    @cached_property
    def _c(self):
        return matrix((1,) * self.n ** 2)

    @cached_property
    def _x(self):
        d = self.n ** 2
        x = ilp(
            c=self._c,
            G=self._G,
            h=self._h,
            A=self._A,
            b=self._b,
            I=set(range(d)),
        )[1]
        return x

    @cached_property
    def _X(self):
        X = matrix(
            [
                [self._x[self.n * j + i] for j in range(self.n)]
                for i in range(self.n)
            ]
        )

        if not self.check(X):
            raise ValueError("Incorrect solution produced")
        return X

    def check(self, X) -> bool:
        """
        checks, whether X is a solution of the system
            A*x == b,
            G*x <= h,
        or not. (here x is the concatenation of X's lines)
        (we don't care, whether c'*x is minimal or not)
        """
        n, m = X.size
        if n != self.n or m != self.n:
            return False
        x = matrix([X[j, i] for j in range(m) for i in range(n)])
        u = self._A * x - self._b

        return max(u) == 0 and min(u) == 0 and max(self._G * x - self._h) <= 0

    def get_a_solution(self) -> List[List[int]]:
        X = matrix(self._X)
        random.seed()
        for _ in range((self.n ** 5) * 100):
            self._shuffle(X)
        if not self.check(X):
            raise ValueError("Incorrect solution produced")
        return [[int(X[i, j]) for j in range(self.n)] for i in range(self.n)]

    def get_a_transposed_solution(self) -> List[List[int]]:
        X = matrix(self._X)
        random.seed()
        for _ in range((self.n ** 5) * 100):
            self._shuffle(X)
        if not self.check(X):
            raise ValueError("Incorrect solution produced")
        return [[int(X[j, i]) for j in range(self.n)] for i in range(self.n)]

    def _shuffle(self, X):
        # Looking for items so that we can move from (i0,j0) some integer into
        # (i0,j1) and we can return the same value (i1,j1) -> (i1, j0)
        i0, i1 = random.sample(range(self.n), 2)
        if self.n > 2:
            j0, j1 = random.sample(range(self.n - 1), 2)
        else:
            j0, j1 = random.sample(range(self.n), 2)
        moveable = min(
            X[i0, j0],
            X[i1, j1],
            self.s[j0] - X[i1, j0],
            self.s[j1] - X[i0, j1],
        )
        if moveable <= 0:
            return
        to_move = random.randint(0, moveable)
        # X[i0,j0] -> X[i0,j1]
        X[i0, j0] -= to_move
        X[i0, j1] += to_move
        # X[i1,j1] -> X[i1,j0]
        X[i1, j1] -= to_move
        X[i1, j0] += to_move


class Problem_B:
    """
    Labels s items with len(a) labels, so that each item has k labels
    """

    def __init__(self, s: int, k: int, a):
        self.s = s
        self.k = k
        self.a = a

    def check(self):
        return sum(self.a) == self.s * self.k and all(
            (a_i < self.s for a_i in self.a)
        )

    @cached_property
    def items(self):
        if self.s == 0:
            return {}
        items = {i: [] for i in range(self.s)}
        free_places = set(range(self.s))
        for i, a_i in enumerate(self.a):
            m = len(free_places)
            rest = a_i
            bound_places = set()
            if a_i > m:
                rest -= m
                for j in free_places:
                    items[j].append(i)
                bound_places = free_places
                free_places = set(range(self.s)) - bound_places
            chosen = random.sample(free_places, rest)
            free_places -= set(chosen)
            free_places |= bound_places
            for j in chosen:
                items[j].append(i)

        return items


def create_labeling(labels: Dict[str, int], intersections: List[int]):
    """
    Creates labeled items using labels[label] pieces of label, so that the
    number of items having i labels is intersections[i-1]
    """

    p1 = Problem_A(labels.values(), intersections)
    items = []
    label_names = list(labels.keys())
    for k, a_k in enumerate(p1.get_a_transposed_solution()):
        p2 = Problem_B(sum(a_k) // (k + 1), k + 1, a_k)
        counter = len(items)
        items += [
            [label_names[i] for i in value] for value in p2.items.values()
        ]
    return items
