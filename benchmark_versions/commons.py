"""
This file contains the same content as its equivalent in the algorithms directory, extended with the functionality
of counting element comparisons for benchmarking purposes. Effectively, this means that the functions return
an additional integer representing the count of performed comparisons. For further documentation and explanation,
check the original algorithms in the algorithms directory.
"""

from typing import TypeVar, List, Tuple

# Generic type of elements in the input list
T = TypeVar('T')


class Run:
    def __init__(self, start: int, end: int) -> None:
        self.start = start
        self.end = end

    def __len__(self) -> int:
        return self.end - self.start + 1

    def __str__(self) -> str:
        return f"({self.start}, {self.end})"


def find_runs(arr: List[T], min_run_length: int | None = None) -> Tuple[List[Run], int]:
    comparisons = 0
    runs = []
    start = 0
    while start < len(arr):
        run, diff = find_next_run(arr, start, min_run_length)
        comparisons += diff
        runs.append(run)
        start = run.end + 1
    return runs, comparisons


def find_next_run(arr: List[T], start: int, min_run_length: int | None = None) -> Tuple[Run, int]:
    end, comparisons = _find_next_natural_run(arr, start)
    run_size = end - start + 1
    if min_run_length and run_size < min_run_length:
        natural_end = end
        end = min(start + min_run_length - 1, len(arr) - 1)
        comparisons += binary_insertion_sort(arr, start, end, natural_end)
    return Run(start, end), comparisons


def _find_next_natural_run(arr: List[T], start: int) -> Tuple[int, int]:
    comparisons = 0
    i = start
    while i < len(arr)-1:
        # Ascending run
        comparisons += 1
        if arr[i] > arr[i+1]:
            break
        i += 1
    comparisons += 1
    if arr[start] == arr[i]:
        while i < len(arr)-1:
            # Descending run
            comparisons += 1
            if arr[i] < arr[i+1]:
                break
            i += 1
        arr[start:i+1] = reversed(arr[start:i+1])
    return i, comparisons


def binary_insertion_sort(arr: List[T], left: int, right: int, m: int) -> int:
    comparisons = 0
    # Inserts elements on indices (m, right) one by one
    for i in range(m+1, right+1):
        val = arr[i]
        j, diff = binary_search(arr, val, left, i)
        comparisons += diff
        arr[j+1:i+1] = arr[j:i]
        arr[j] = val
    return comparisons


def binary_search(arr: List[T], val: T, start: int, end: int) -> Tuple[int, int]:
    comparisons = 0
    while start < end:
        mid = (start+end) // 2
        if arr[mid] < val:
            start = mid+1
        else:
            end = mid
        comparisons += 1
    return start, comparisons


def merge(arr: List[T], l: int, m: int, r: int) -> Tuple[Run, int]:
    comparisons = 0
    left = arr[l:m+1]     # first run
    right = arr[m+1:r+1]  # second run
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
        comparisons += 1
    while i < len(left):
        arr[k] = left[i]
        i += 1
        k += 1
    while j < len(right):
        arr[k] = right[j]
        j += 1
        k += 1
    return Run(l, r), comparisons
