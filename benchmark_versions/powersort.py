"""
This file contains the same content as its equivalent in the algorithms directory, extended with the functionality
of counting element comparisons for benchmarking purposes. Effectively, this means that the functions return
an additional integer representing the count of performed comparisons. For further documentation and explanation,
check the original algorithms in the algorithms directory.
"""

from typing import List, TypeVar, Tuple

from benchmark_versions.commons import merge, find_next_run, Run

# Generic type of elements in the input list
T = TypeVar('T')


def powersort(arr: List[T], min_run_length: int | None = None,
              galloping_enabled: bool = False,
              galloping_dynamic_threshold_enabled: bool = False) -> Tuple[List[T], int]:
    n = len(arr)
    X = []
    P = []
    r1, comparisons = find_next_run(arr, 0, min_run_length)  # current run
    while r1.end < n - 1:
        r2, diff = find_next_run(arr, r1.end + 1, min_run_length)  # next run
        comparisons += diff
        p = node_power(r1, r2, n)
        while P and P[-1] > p:
            P.pop()
            r0 = X.pop()  # previous run on the stack
            r1, diff = merge(arr, r0.start, r0.end, r1.end, galloping_enabled, galloping_dynamic_threshold_enabled)
            comparisons += diff
        X.append(r1)
        P.append(p)
        r1 = r2
    while X:
        r0 = X.pop()
        r1, diff = merge(arr, r0.start, r0.end, r1.end, galloping_enabled, galloping_dynamic_threshold_enabled)
        comparisons += diff
    return arr, comparisons


def node_power(r1: Run, r2: Run, n: int) -> int:
    n1 = r1.end - r1.start + 1
    n2 = r2.end - r2.start + 1
    l = 0
    a = (r1.start + n1 / 2 - 1) / n
    b = (r2.start + n2 / 2 - 1) / n
    while int(a * 2**l) == int(b * 2**l):
        l += 1
    return l
