import random

from algorithms.natural_merge_sort import natural_merge_sort
from algorithms.powersort import powersort
from algorithms.timsort import timsort

from benchmark_versions.merge_sort import merge_sort as benchmark_merge_sort
from benchmark_versions.natural_merge_sort import natural_merge_sort as benchmark_natural_merge_sort
from benchmark_versions.timsort import timsort as benchmark_timsort
from benchmark_versions.powersort import powersort as benchmark_powersort


if __name__ == '__main__':
    for _ in range(100):
        arr = [random.randint(0, 1000) for _ in range(1000)]
        sorted_arr = sorted(arr)
        assert sorted_arr == natural_merge_sort(arr.copy())
        assert sorted_arr == timsort(arr.copy())
        assert sorted_arr == powersort(arr.copy(), min_run_length=32)
        assert sorted_arr == powersort(arr.copy(), min_run_length=None)

        assert sorted_arr == benchmark_merge_sort(arr.copy())[0]
        assert sorted_arr == benchmark_natural_merge_sort(arr.copy())[0]
        assert sorted_arr == benchmark_timsort(arr.copy())[0]
        assert sorted_arr == benchmark_powersort(arr.copy(), min_run_length=32)[0]
        assert sorted_arr == benchmark_powersort(arr.copy(), min_run_length=None)[0]
