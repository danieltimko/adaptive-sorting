from typing import TypeVar, List, Tuple


T = TypeVar('T')


def natural_merge_sort(arr: List[T]) -> Tuple[List[T], int]:
    """
    TODO
    """

    if len(arr) <= 1:
        return arr, 0

    runs, comparisons = find_runs(arr)
    while len(runs) > 1:
        new_runs = []
        i = 0
        while i < len(runs)-1:
            l, m = runs[i]
            _, r = runs[i+1]
            comparisons += merge(arr, l, m, r)
            new_runs.append((l, r))
            i += 2
        if i == len(runs)-1:
            new_runs.append(runs[-1])
        runs = new_runs
    return arr, comparisons


def find_runs(arr: List[T]) -> Tuple[List[Tuple[int, int]], int]:
    comparisons = 0
    runs = []
    i = 0
    while i < len(arr):
        start = i
        # Ascending run?
        while i < len(arr)-1:
            comparisons += 1
            if arr[i] > arr[i+1]:
                break
            i += 1
        # Descending run?
        if arr[start] == arr[i]:
            while i < len(arr)-1:
                comparisons += 1
                if arr[i] < arr[i+1]:
                    break
                i += 1
            arr[start:i+1] = reversed(arr[start:i+1])
        runs.append((start, i+1))
        i += 1
    return runs, comparisons


def merge(arr: List[T], l: int, m: int, r: int) -> int:
    comparisons = 0
    left = arr[l:m]
    right = arr[m:r]
    k = l
    i = 0
    j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        k += 1
        comparisons += 1
    while i < len(left):
        arr[k] = left[i]
        i += 1
        k += 1
    while j < len(right):
        arr[k] = right[j]
        j += 1
        k += 1
    return comparisons
