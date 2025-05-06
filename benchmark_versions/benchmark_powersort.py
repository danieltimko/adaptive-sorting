from typing import TypeVar, List, Tuple

T = TypeVar('T')


def powersort(arr: List[T], fix_minrun: bool = True) -> Tuple[List[T], int]:
    """
    TODO
    """

    n = len(arr)
    X = []
    P = []
    s1 = 0
    e1, comparisons = find_next_run(arr, 0, fix_minrun)
    while e1 < n - 1:
        s2 = e1 + 1
        e2, comp = find_next_run(arr, s2, fix_minrun)
        comparisons += comp
        p = node_power(s1, e1, s2, e2, n)
        while P and P[-1] > p:
            P.pop()
            s1, e1, comp = merge(arr, *X.pop(), e1)
            comparisons += comp
        X.append((s1, e1))
        P.append(p)
        s1 = s2
        e1 = e2
    while X:
        s1, e1, comp = merge(arr, *X.pop(), e1)
        comparisons += comp
    return arr, comparisons


def find_next_run(arr: List[T], start: int, fix_minrun: bool = True) -> Tuple[int, int]:
    comparisons = 0
    end, comp = _find_next_run(arr, start)
    comparisons += comp
    if fix_minrun:
        MIN_RUN = 32
        run_size = end - start + 1
        if run_size < MIN_RUN:
            # Extend run to length MIN_RUN
            end = min(start + MIN_RUN - 1, len(arr) - 1)
            comp = binary_insertion_sort(arr, start, end, start)
            comparisons += comp
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


def _find_next_run(arr: List[T], start: int) -> Tuple[int, int]:
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


def node_power(s1: int, e1: int, s2: int, e2: int, n: int) -> int:
    n1 = e1 - s1 + 1
    n2 = e2 - s2 + 1
    l = 0
    a = (s1 + n1/2 - 1)/n
    b = (s2 + n2/2 - 1)/n
    while int(a * 2**l) == int(b * 2**l):
        l += 1
    return l


def merge(arr: List[T], left: int, mid: int, right: int) -> Tuple[int, int, int]:
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
    return left, right, comparisons
