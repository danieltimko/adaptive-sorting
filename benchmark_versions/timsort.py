"""
This file contains the same content as its equivalent in the algorithms directory, extended with the functionality
of counting element comparisons for benchmarking purposes. Effectively, this means that the functions return
an additional integer representing the count of performed comparisons. For further documentation and explanation,
check the original algorithms in the algorithms directory.
"""

from typing import TypeVar, List, Tuple

from benchmark_versions.commons import merge, find_runs

# Generic type of elements in the input list
T = TypeVar('T')


def timsort(arr: List[T]) -> Tuple[List[T], int]:
    MIN_RUN = 32
    runs, comparisons = find_runs(arr, min_run_length=MIN_RUN)
    S = []
    for run in runs:
        S.append(run)
        while True:
            h = len(S)
            r1 = S[-1]
            r2 = S[-2] if h >= 2 else None
            r3 = S[-3] if h >= 3 else None
            r4 = S[-4] if h >= 4 else None

            def merge12() -> int:
                # Merge r1 and r2
                S.pop(), S.pop()
                r, diff = merge(arr, r2.start, r2.end, r1.end)
                S.append(r)
                return diff

            def merge23() -> int:
                # Merge r2 and r3
                S.pop(), S.pop(), S.pop()
                r, diff = merge(arr, r3.start, r3.end, r2.end)
                S.append(r)
                S.append(r1)
                return diff

            # Merging on-the-fly
            if h >= 3 and len(r1) >= len(r3):
                comparisons += merge23()
            elif h >= 2 and len(r1) >= len(r2):
                comparisons += merge12()
            elif h >= 3 and len(r1) + len(r2) >= len(r3):
                comparisons += merge12()
            elif h >= 4 and len(r2) + len(r3) >= len(r4):
                comparisons += merge12()
            else:
                break
    while len(S) > 1:
        r1, r2 = S.pop(), S.pop()
        run, diff = merge(arr, r2.start, r2.end, r1.end)
        comparisons += diff
        S.append(run)
    return arr, comparisons
