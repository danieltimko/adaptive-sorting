"""
This file contains the same content as its equivalent in the algorithms directory, extended with the functionality
of counting element comparisons for benchmarking purposes. Effectively, this means that the functions return
an additional integer representing the count of performed comparisons. For further documentation and explanation,
check the original algorithms in the algorithms directory.
"""

from typing import List, TypeVar, Tuple

from benchmark_versions.commons import merge, find_runs

# Generic type of elements in the input list
T = TypeVar('T')


def natural_merge_sort(arr: List[T]) -> Tuple[List[T], int]:
    """
    Sorts the input list using Natural Merge Sort algorithm.

    :param arr: Input sequence to sort
    :return: Sorted sequence (increasing)
    """

    if len(arr) <= 1:
        return arr, 0

    runs, comparisons = find_runs(arr)
    while len(runs) > 1:
        new_runs = []
        i = 0
        while i < len(runs)-1:
            r1 = runs[i]
            r2 = runs[i+1]
            run, diff = merge(arr, r1.start, r1.end, r2.end)
            comparisons += diff
            new_runs.append(run)
            i += 2
        if i == len(runs)-1:
            new_runs.append(runs[-1])
        runs = new_runs
    return arr, comparisons
