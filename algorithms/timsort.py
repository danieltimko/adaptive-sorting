from typing import TypeVar, List

from algorithms.commons import merge, find_runs
from config import MIN_RUN

# Generic type of elements in the input list
T = TypeVar('T')


def timsort(arr: List[T]) -> List[T]:
    """
    Sorts the input list using Timsort algorithm.

    Note that this implementation of Timsort does not include *all* performance
    optimizations proposed by Tim Peters.
    See https://svn.python.org/projects/python/trunk/Objects/listsort.txt
    The implemented optimizations: MIN_RUN, binary insertion sort, galloping mode (TODO)

    :param arr: Input sequence to sort
    :return: Sorted sequence (increasing)
    """

    runs = find_runs(arr, min_run_length=MIN_RUN)
    S = []
    for run in runs:
        S.append(run)
        while True:
            h = len(S)
            r1 = S[-1]
            r2 = S[-2] if h >= 2 else None
            r3 = S[-3] if h >= 3 else None
            r4 = S[-4] if h >= 4 else None

            def merge12():
                # Merge r1 and r2
                S.pop(), S.pop()
                S.append(merge(arr, r2.start, r2.end, r1.end))

            def merge23():
                # Merge r2 and r3
                S.pop(), S.pop(), S.pop()
                S.append(merge(arr, r3.start, r3.end, r2.end))
                S.append(r1)

            # Merging on-the-fly
            if h >= 3 and len(r1) >= len(r3):
                merge23()
            elif h >= 2 and len(r1) >= len(r2):
                merge12()
            elif h >= 3 and len(r1) + len(r2) >= len(r3):
                merge12()
            elif h >= 4 and len(r2) + len(r3) >= len(r4):
                merge12()
            else:
                break
    while len(S) > 1:
        r1, r2 = S.pop(), S.pop()
        S.append(merge(arr, r2.start, r2.end, r1.end))
    return arr
