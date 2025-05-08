from typing import TypeVar, List


# Generic type of elements in the input list
T = TypeVar('T')


class Run:
    """
    Object representation of a run, which is effectively a sorted subarray.
    It is defined by its start and end indices in the array.
    """

    def __init__(self, start: int, end: int) -> None:
        """
        Constructor creating the representation of the run [start, end].

        :param start: Index on which the run begins (inclusive)
        :param end: Index on which the run ends (inclusive)
        """
        self.start = start
        self.end = end

    def __len__(self) -> int:
        return self.end - self.start + 1

    def __str__(self) -> str:
        return f"({self.start}, {self.end})"


def find_runs(arr: List[T], min_run_length: int | None = None) -> List[Run]:
    """
    Finds the run decomposition of the input sequence.
    Supports detecting both ascending and descending runs.
    Additionally, the function optionally enforces the minimal run length policy, extending
    all natural runs shorter than min_run_length, using Binary Insertion Sort.

    :param arr: Input sequence
    :param min_run_length: (optional) Minimal length of runs to enforce
    :return: List of runs
    """

    runs = []
    start = 0
    while start < len(arr):
        run = find_next_run(arr, start, min_run_length)
        runs.append(run)
        start = run.end + 1
    return runs


def find_next_run(arr: List[T], start: int, min_run_length: int | None = None) -> Run:
    """
    Finds the end of the run (ascending or descending) starting on the specified index.
    Additionally, the function optionally enforces the minimal run length policy, extending
    all natural runs shorter than MIN_RUN, using Binary Insertion Sort.

    :param arr: Input sequence
    :param start: Index on which the run begins
    :param min_run_length: (optional) Minimal length of runs to enforce
    :return: Representation of the found run
    """

    end = _find_next_natural_run(arr, start)
    run_size = end - start + 1
    if min_run_length and run_size < min_run_length:
        natural_end = end
        end = min(start + min_run_length - 1, len(arr) - 1)
        binary_insertion_sort(arr, start, end, natural_end)
    return Run(start, end)


def _find_next_natural_run(arr: List[T], start: int) -> int:
    """
    Finds the end of the natural run (ascending or descending) starting on the specified index.
    The descending runs are reversed in-place, in order to work exclusively with ascending
    runs for simplicity.

    :param arr: Input sequence
    :param start: Index on which the run begins
    :return: Index on which the run ends (inclusive)
    """

    i = start
    while i < len(arr)-1 and arr[i] <= arr[i+1]:
        # Ascending run
        i += 1
    if arr[start] == arr[i]:
        while i < len(arr)-1 and arr[i] >= arr[i+1]:
            # Descending run
            i += 1
        arr[start:i+1] = reversed(arr[start:i+1])
    return i


def binary_insertion_sort(arr: List[T], left: int, right: int, m: int) -> None:
    """
    Sorts the specified subarray using Binary Insertion Sort algorithm.
    This function assumes that the [left, m] part of the subarray is already sorted.

    :param arr: Input sequence
    :param left: Start index of the subarray to sort
    :param right: End index of the subarray to sort
    :param m: Last index of the sorted part of the subarray
    :return: None
    """

    # Inserts elements on indices (m, right) one by one
    for i in range(m+1, right+1):
        val = arr[i]
        j = binary_search(arr, val, left, i)
        arr[j+1:i+1] = arr[j:i]
        arr[j] = val


def binary_search(arr: List[T], val: T, start: int, end: int) -> int:
    """
    Finds the correct position in the subarray for the specified value using binary search.
    Note that the element does not have to exist in the array.

    :param arr: Input sequence
    :param val: Value to find the correct position for
    :param start: Start index of the search context
    :param end: End index of the search context
    :return: Index of the correct position for the specified value
    """

    while start < end:
        mid = (start+end) // 2
        if arr[mid] < val:
            start = mid+1
        else:
            end = mid
    return start


def merge(arr: List[T], l: int, m: int, r: int) -> Run:
    """
    Merges two adjacent runs of the input sequence in-place.
    Analogous to the linear-time merge operation of the traditional Merge Sort.

    :param arr: Input sequence
    :param l: (left) Starting index of the first run (inclusive)
    :param m: (middle) Ending index of the first run (inclusive), starting index of the second run (exclusive)
    :param r: (right) Ending index of the second run (inclusive)
    :return: New merged run: [left, right]
    """

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
    while i < len(left):
        arr[k] = left[i]
        i += 1
        k += 1
    while j < len(right):
        arr[k] = right[j]
        j += 1
        k += 1
    return Run(l, r)
