from typing import List, TypeVar

from algorithms.commons import merge, find_next_run, Run

# Generic type of elements in the input list
T = TypeVar('T')


def powersort(arr: List[T], min_run_length: int | None = None, galloping_enabled: bool = False,
              galloping_dynamic_threshold_enabled: bool = False) -> List[T]:
    """
    Sorts the input list using Powersort algorithm.

    This implementation can leverage the same optimization techniques as Timsort (timsort.py):
    MIN_RUN, binary insertion sort, galloping mode.
    They are implemented as optional, in order to be able to test the performance of Powersort with and without them.

    :param arr: Input sequence to sort
    :param min_run_length: (optional) Minimal length of runs to enforce (and use binary insertion sort for shorter runs)
    :param galloping_enabled: (optional) Whether entering the galloping mode is enabled or not; Default: false
    :param galloping_dynamic_threshold_enabled: (optional) Whether dynamic tuning of the galloping threshold
        is enabled or not; If true, the threshold decreases with every successful gallop, and decreases with every
        unsuccessful one. If false, the threshold stays always the same. Default: false
    :return: Sorted sequence (increasing)
    """

    n = len(arr)
    X = []
    P = []
    r1 = find_next_run(arr, 0, min_run_length)  # current run
    while r1.end < n - 1:
        r2 = find_next_run(arr, r1.end + 1, min_run_length)  # next run
        p = node_power(r1, r2, n)
        while P and P[-1] > p:
            P.pop()
            r0 = X.pop()  # previous run on the stack
            r1 = merge(arr, r0.start, r0.end, r1.end, galloping_enabled, galloping_dynamic_threshold_enabled)
        X.append(r1)
        P.append(p)
        r1 = r2
    while X:
        r0 = X.pop()
        r1 = merge(arr, r0.start, r0.end, r1.end, galloping_enabled, galloping_dynamic_threshold_enabled)
    return arr


def node_power(r1: Run, r2: Run, n: int) -> int:
    """
    Calculates the power of the run boundary of the two runs.

    :param r1: First run
    :param r2: Second run
    :param n: Length of the input array
    :return: Internal node power of the two runs
    """

    n1 = r1.end - r1.start + 1
    n2 = r2.end - r2.start + 1
    l = 0
    a = (r1.start + n1 / 2 - 1) / n
    b = (r2.start + n2 / 2 - 1) / n
    while int(a * 2**l) == int(b * 2**l):
        l += 1
    return l
