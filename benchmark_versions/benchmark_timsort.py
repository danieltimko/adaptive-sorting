from typing import TypeVar, List, Tuple

T = TypeVar('T')


class Run:
    # TODO add this also to benchmark_powersort
    def __init__(self, low: int, high: int) -> None:
        self.low = low
        self.high = high

    def __len__(self) -> int:
        return self.high - self.low + 1

    def __str__(self) -> str:
        return f"({self.low}, {self.high})"


def timsort(arr: List[T]) -> Tuple[List[T], int]:
    runs, comparisons = find_runs(arr)
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
                comp = merge(arr, r2.low, r2.high, r1.high)
                S.append(Run(r2.low, r1.high))
                return comp

            def merge23() -> int:
                # Merge r2 and r3
                S.pop(), S.pop(), S.pop()
                comp = merge(arr, r3.low, r3.high, r2.high)
                S.append(Run(r3.low, r2.high))
                S.append(r1)
                return comp

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
        comparisons += merge(arr, r2.low, r2.high, r1.high)
        S.append(Run(r2.low, r1.high))
    return arr, comparisons


def find_runs(arr: List[T]) -> Tuple[List[Run], int]:
    comparisons = 0
    MIN_RUN = 32  # TODO parametrize
    runs = []
    i = 0
    while i < len(arr):
        j, comp = find_next_natural_run(arr, i)
        comparisons += comp
        run_size = j - i + 1
        if run_size < MIN_RUN:
            # Extend run to length MIN_RUN
            end_index = min(i + MIN_RUN - 1, len(arr) - 1)
            diff = binary_insertion_sort(arr, i, end_index, j)
            comparisons += diff
            j = end_index
        runs.append(Run(i, j))
        i = j + 1
    return runs, comparisons


def find_next_natural_run(arr: List[T], start: int) -> Tuple[int, int]:
    comparisons = 0
    end = start
    while end < len(arr)-1:
        comparisons += 1
        if arr[end] != arr[end+1]:
            break
        end += 1
    tmp = end
    while end < len(arr)-1:
        # Ascending run
        comparisons += 1
        if arr[end] > arr[end+1]:
            break
        end += 1
    if end == tmp:
        # Descending run
        while end < len(arr)-1:
            comparisons += 1
            if arr[end] < arr[end+1]:
                break
            end += 1
        arr[start:end+1] = reversed(arr[start:end+1])
    return end, comparisons


def binary_insertion_sort(arr: List[T], left: int, right: int, m: int) -> int:
    comparisons = 0
    for i in range(m+1, right+1):
        val = arr[i]
        j, comp = binary_search(arr, val, left, i)
        comparisons += comp
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


def merge(arr: List[T], left: int, mid: int, right: int) -> int:
    comparisons = 0
    left_part = arr[left:mid+1]
    right_part = arr[mid+1:right+1]
    l, r = 0, 0
    i = left
    while l < len(left_part) and r < len(right_part):
        if left_part[l] <= right_part[r]:
            arr[i] = left_part[l]
            l += 1
        else:
            arr[i] = right_part[r]
            r += 1
        i += 1
        comparisons += 1
    while l < len(left_part):
        arr[i] = left_part[l]
        l += 1
        i += 1
    while r < len(right_part):
        arr[i] = right_part[r]
        r += 1
        i += 1
    return comparisons
