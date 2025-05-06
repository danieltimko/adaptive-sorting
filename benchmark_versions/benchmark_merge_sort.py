from typing import TypeVar, List, Tuple

T = TypeVar('T')


def merge_sort(arr: List[T]) -> Tuple[List[T], int]:
    if len(arr) <= 1:
        return arr, 0
    comparisons = 0
    m = len(arr) // 2
    left, comp = merge_sort(arr[:m])
    comparisons += comp
    right, comp = merge_sort(arr[m:])
    comparisons += comp
    merged, comp = merge(left, right)
    return merged, comparisons + comp


def merge(left: List[T], right: List[T]) -> Tuple[List[T], int]:
    comparisons = 0
    arr = []
    li = 0
    ri = 0
    while li < len(left) and ri < len(right):
        if left[li] <= right[ri]:
            arr.append(left[li])
            li += 1
        else:
            arr.append(right[ri])
            ri += 1
        comparisons += 1
    while li < len(left):
        arr.append(left[li])
        li += 1
    while ri < len(right):
        arr.append(right[ri])
        ri += 1
    return arr, comparisons
