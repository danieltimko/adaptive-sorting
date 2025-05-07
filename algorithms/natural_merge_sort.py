from typing import List, Tuple, TypeVar


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

    runs = _find_runs(arr)
    while len(runs) > 1:
        new_runs = []
        i = 0
        while i < len(runs)-1:
            l, m = runs[i]
            _, r = runs[i+1]
            _merge(arr, l, m, r)
            new_runs.append((l, r))
            i += 2
        if i == len(runs)-1:
            new_runs.append(runs[-1])
        runs = new_runs
    return arr


def _find_runs(arr: List[T]) -> List[Tuple[int, int]]:
    """
    Finds the run decomposition of the input sequence.
    Supports detecting both ascending and descending runs. More precisely,
    it reverses the descending runs in-place, in order to work exclusively
    with ascending runs for simplicity.

    :param arr: Input sequence
    :return: List of runs represented as pairs of indices [start, end)
    """

    runs = []
    i = 0
    while i < len(arr):
        start = i
        # Ascending run?
        while i < len(arr)-1 and arr[i] <= arr[i+1]:
            i += 1
        # Descending run?
        if arr[start] == arr[i]:
            while i < len(arr)-1 and arr[i] >= arr[i+1]:
                i += 1
            arr[start:i+1] = reversed(arr[start:i+1])
        runs.append((start, i+1))
        i += 1
    return runs


def _merge(arr: List[T], l: int, m: int, r: int) -> None:
    """
    Merges two adjacent runs of the input sequence in-place.

    :param arr: Input sequence
    :param l: (left) Starting index of the first run
    :param m: (middle) Ending index of the first run, starting index of the second run
    :param r: (right) Ending index of the second run
    """

    left = arr[l:m]   # first run
    right = arr[m:r]  # second run
    k = l  # index in the original array
    i = 0  # index in the first run
    j = 0  # index in the second run
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        k += 1
    while i < len(left):
        arr[k] = left[i]
        i += 1
        k += 1
    while j < len(right):
        arr[k] = right[j]
        j += 1
        k += 1
