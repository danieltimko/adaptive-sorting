from typing import List, TypeVar, Tuple


# Generic type of elements in the input list
T = TypeVar('T')


class Run:
    """
    TODO
    """

    def __init__(self, low: int, high: int) -> None:
        self.start = low
        self.end = high

    def __len__(self) -> int:
        return self.end - self.start + 1

    def __str__(self) -> str:
        return f"({self.start}, {self.end})"


def powersort(arr: List[T], fix_minrun: bool = True) -> List[T]:
    """
    Sorts the input list using Powersort algorithm.

    This implementation can leverage the same optimization techniques as Timsort (timsort.py):
    MIN_RUN=32, binary insertion sort, galloping mode (TODO)

    :param arr: Input sequence to sort
    :param fix_minrun: Whether to enforce minimal run length (and use binary insertion sort for smaller runs)
    :return: Sorted sequence (increasing)
    """

    n = len(arr)
    X = []
    P = []
    r1 = _find_next_run(arr, 0, fix_minrun)  # current run
    while r1.end < n - 1:
        r2 = _find_next_run(arr, r1.start + 1, fix_minrun)  # next run
        p = node_power(r1, r2, n)
        while P and P[-1] > p:
            P.pop()
            r0 = X.pop()  # previous run on the stack
            s1, e1 = _merge(arr, r0.start, r0.end, r1.end)
        X.append(r1)
        P.append(p)
        r1 = r2
    while X:
        r0 = X.pop()
        r1 = _merge(arr, r0.start, r0.end, r1.end)
    return arr


def _find_next_run(arr: List[T], start: int, fix_minrun: bool = True) -> Run:
    """
    TODO

    :param fix_minrun: Whether to enforce minimal run length (and use binary insertion sort for smaller runs)

    """

    end = _find_next_natural_run(arr, start)
    if fix_minrun:
        MIN_RUN = 32
        run_size = end - start + 1
        if run_size < MIN_RUN:
            end = min(start + MIN_RUN - 1, len(arr) - 1)
            binary_insertion_sort(arr, start, end, start)
    return Run(start, end)


def binary_insertion_sort(arr: List[T], left: int, right: int, m: int) -> None:
    """
    TODO
    """

    for i in range(m+1, right+1):
        val = arr[i]
        j = binary_search(arr, val, left, i)
        arr[j+1:i+1] = arr[j:i]
        arr[j] = val


def binary_search(arr: List[T], val: T, start: int, end: int) -> int:
    """
    TODO
    """

    while start < end:
        mid = (start+end) // 2
        if arr[mid] < val:
            start = mid+1
        else:
            end = mid
    return start


def _find_next_natural_run(arr: List[T], start: int) -> int:
    """
    TODO
    """

    end = start
    while end < len(arr)-1 and arr[end] == arr[end+1]:
        end += 1
    tmp = end
    while end < len(arr)-1 and arr[end] <= arr[end+1]:
        # Ascending run
        end += 1
    if end == tmp:
        # Descending run
        while end < len(arr)-1 and arr[end] >= arr[end+1]:
            end += 1
        arr[start:end+1] = reversed(arr[start:end+1])
    return end


def node_power(r1: Run, r2: Run, n: int) -> int:
    """
    TODO
    """

    n1 = r1.end - r1.start + 1
    n2 = r2.end - r2.start + 1
    l = 0
    a = (r1.start + n1 / 2 - 1) / n
    b = (r2.start + n2 / 2 - 1) / n
    while int(a * 2**l) == int(b * 2**l):
        l += 1
    return l


def _merge(arr: List[T], left: int, mid: int, right: int) -> Tuple[int, int]:
    """
    TODO
    """

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
    while l < len(left_part):
        arr[i] = left_part[l]
        l += 1
        i += 1
    while r < len(right_part):
        arr[i] = right_part[r]
        r += 1
        i += 1
    return left, right
