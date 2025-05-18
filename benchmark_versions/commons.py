"""
This file contains the same content as its equivalent in the algorithms directory, extended with the functionality
of counting element comparisons for benchmarking purposes. Effectively, this means that the functions return
an additional integer representing the count of performed comparisons. For further documentation and explanation,
check the original algorithms in the algorithms directory.
"""

from typing import TypeVar, List, Tuple

from config import INITIAL_GALLOPING_THRESHOLD

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


def merge(arr: List[T], l: int, m: int, r: int,
          galloping_enabled: bool = False,
          galloping_dynamic_threshold_enabled: bool = False) -> Tuple[Run, int]:
    comparisons = 0
    left = arr[l:m+1]     # first run
    right = arr[m+1:r+1]  # second run
    k = l  # index in the original array
    i = 0  # index in the first run
    j = 0  # index in the second run

    galloping_threshold = INITIAL_GALLOPING_THRESHOLD  # initial threshold to trigger the galloping mode
    win_count = 0  # how many times consecutively was the element picked from the same run (winning run)
    left_winning = True  # whether it was the left or the right run

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            arr[k] = left[i]
            i += 1
            if left_winning:
                win_count += 1
            else:
                win_count = 1
                left_winning = True
        else:
            arr[k] = right[j]
            j += 1
            if left_winning:
                win_count = 1
                left_winning = False
            else:
                win_count += 1
        k += 1
        comparisons += 1

        # Do not start galloping if one of the runs is already exhausted
        if i >= len(left) or j >= len(right):
            break

        # Trigger galloping mode?
        if galloping_enabled and win_count >= galloping_threshold:
            if left_winning:
                # Gallop in left run
                idx, diff = _gallop(left, i, right[j], True)
                galloped = idx - i
                while i < idx:
                    arr[k] = left[i]
                    i += 1
                    k += 1
            else:
                # Gallop in right run
                idx, diff = _gallop(right, j, left[i], False)
                galloped = idx - j
                while j < idx:
                    arr[k] = right[j]
                    j += 1
                    k += 1
            win_count = 0
            comparisons += diff

            # Adaptive tuning of the galloping threshold (based on the number of galloped items)
            if galloping_dynamic_threshold_enabled:
                if galloped >= galloping_threshold:
                    galloping_threshold = max(1, galloping_threshold - 1)
                else:
                    galloping_threshold += 2

    # Final copying
    while i < len(left):
        arr[k] = left[i]
        i += 1
        k += 1
    while j < len(right):
        arr[k] = right[j]
        j += 1
        k += 1
    return Run(l, r), comparisons


def _gallop(run, start, val, incl_eq):
    l = start
    r = len(run)
    if l == r:
        return l, 0
    if (incl_eq and run[l] > val) or (not incl_eq and run[l] >= val):
        return l, 1
    comparisons = 1
    # Exponential search
    size = 1
    while l+size < r and ((incl_eq and run[l+size] <= val) or (not incl_eq and run[l+size] < val)):
        size *= 2
        comparisons += 1
    comparisons += 1
    l += size//2
    r = min(l+size, r)
    # Binary search
    while l < r:
        mid = (l+r) // 2
        comparisons += 1
        if (incl_eq and run[mid] <= val) or (not incl_eq and run[mid] < val):
            l = mid + 1
        else:
            r = mid
    return r, comparisons
