from typing import List, TypeVar

from algorithms.commons import merge, find_runs

# Generic type of elements in the input list
T = TypeVar('T')


def natural_merge_sort(arr: List[T]) -> List[T]:
    """
    Sorts the input list using Natural Merge Sort algorithm.

    :param arr: Input sequence to sort
    :return: Sorted sequence (increasing)
    """

    if len(arr) <= 1:
        return arr

    runs = find_runs(arr)
    while len(runs) > 1:
        new_runs = []
        i = 0
        while i < len(runs)-1:
            r1 = runs[i]
            r2 = runs[i+1]
            new_runs.append(merge(arr, r1.start, r1.end, r2.end))
            i += 2
        if i == len(runs)-1:
            new_runs.append(runs[-1])
        runs = new_runs
    return arr
