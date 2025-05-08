from typing import TypeVar, List, Tuple


# Generic type of elements in the input list
T = TypeVar('T')


def merge_sort(arr: List[T]) -> Tuple[List[T], int]:
    """
    Sorts the input list using traditional top-down Merge Sort algorithm.

    :param arr: Input sequence to sort
    :return: Sorted sequence (increasing), along with the count of performed element comparisons
    """

    if len(arr) <= 1:
        return arr, 0
    comparisons = 0
    m = len(arr) // 2
    left, diff = merge_sort(arr[:m])
    comparisons += diff
    right, diff = merge_sort(arr[m:])
    comparisons += diff
    merged, diff = merge(left, right)
    return merged, comparisons + diff


def merge(left: List[T], right: List[T]) -> Tuple[List[T], int]:
    """
    Merges two sorted arrays into a single one in linear time.

    :param left: First sorted array
    :param right: Second sorted array
    :return: Merged sorted array, along with the count of performed element comparisons
    """
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
