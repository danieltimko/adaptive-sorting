import time
from typing import Callable, Any, List, Tuple, TypeVar

from benchmark_versions.merge_sort import merge_sort
from benchmark_versions.natural_merge_sort import natural_merge_sort
from benchmark_versions.timsort import timsort
from benchmark_versions.powersort import powersort
from config import SIZE_CONFIGURATIONS, N_SAMPLES, RUNS_CONFIGURATIONS, ENTROPY_CONFIGURATIONS, MIN_RUN

from output_generation import plot_results, plot_minrun_results, save_to_csv
from random_input_generators import generate_random_list


# Generic type of elements in the input list
T = TypeVar('T')
# Return type of the benchmarked sorting functions
TResult = Tuple[List[T], int]


def timeit(func: Callable[..., TResult]) -> Callable[..., Tuple[TResult, float]]:
    """
    Decorator function that measures the CPU execution time of the decorated function.

    Note: This was not used in benchmarks, but is left here for reference and potential use.

    :param func: Function whose execution time should be measured
    :return: Wrapper function that returns the original result and the execution time [ms]
    """
    def wrapper(*args, **kwargs) -> Tuple[TResult, float]:
        start_time = time.process_time()
        result = func(*args, **kwargs)
        time_taken = time.process_time() - start_time
        return result, time_taken * 1000
    return wrapper


class Comparable:
    """
    Wrapper class that represents a comparable object.
    It overrides/decorates the object's comparison magic methods to keep the global count
    of comparisons performed on *all* Comparable instances.
    """

    # Static variable to track the number of comparisons
    comparison_count = 0

    def __init__(self, value: Any) -> None:
        self.value = value

    def __lt__(self, other: Any) -> bool:
        Comparable.comparison_count += 1
        return self.value < other.value

    def __le__(self, other: Any) -> bool:
        Comparable.comparison_count += 1
        return self.value <= other.value

    def __gt__(self, other: Any) -> bool:
        Comparable.comparison_count += 1
        return self.value > other.value

    def __ge__(self, other: Any) -> bool:
        Comparable.comparison_count += 1
        return self.value >= other.value

    def __eq__(self, other: Any) -> bool:
        Comparable.comparison_count += 1
        return self.value == other.value

    def __ne__(self, other: Any) -> bool:
        Comparable.comparison_count += 1
        return self.value != other.value


@timeit
def run_python_sort_for_comparisons(arr: List[T]) -> Tuple[TResult, float]:
    """
    Runs the Python reference sorting function (sorted()), extracting the number
    of element comparisons performed during its execution and measuring its CPU execution time.
    It achieves so by wrapping the array's elements in a Comparable class, which
    enables keeping the global comparison counter.

    :param arr: Input sequence to sort
    :return: The number of performed comparisons, along with the execution time [ms]
    """

    Comparable.comparison_count = 0
    wrapped_arr = [Comparable(x) for x in arr]
    sorted_arr = sorted(wrapped_arr)
    return sorted_arr, Comparable.comparison_count


@timeit
def run_timsort(arr: List[T]) -> Tuple[TResult, float]:
    """
    Runs the benchmark version of Timsort and measures its CPU execution time.

    :param arr: Input sequence to sort
    :return: Sorted input along with the number of performed comparisons, along with the execution time [ms]
    """

    return timsort(arr)


@timeit
def run_powersort(arr: List, min_run_length: int | None = MIN_RUN) -> Tuple[List, int]:
    """
    Runs the benchmark version of Powersort and measures its CPU execution time.

    :param arr: Input sequence to sort
    :param min_run_length: (optional) Minimal length of runs to enforce; Default: 32
    :return: Sorted input along with the number of performed comparisons, along with the execution time [ms]
    """

    return powersort(arr, min_run_length)


@timeit
def run_natural_merge_sort(arr: List) -> Tuple[List, int]:
    """
    Runs the benchmark version of Natural Merge Sort and measures its CPU execution time.

    :param arr: Input sequence to sort
    :return: Sorted input along with the number of performed comparisons, along with the execution time [ms]
    """

    return natural_merge_sort(arr)


@timeit
def run_merge_sort(arr: List) -> Tuple[List, int]:
    """
    Runs the benchmark version of Merge Sort and measures its CPU execution time.

    :param arr: Input sequence to sort
    :return: Sorted input along with the number of performed comparisons, along with the execution time [ms]
    """

    return merge_sort(arr)


def benchmark_minrun_impact() -> None:
    """
    Runs the benchmark for MIN_RUN impact in Powersort.
    Measures the performance difference between the Powersort version that uses MIN_RUN=32 (and binary insertion sort
    to handle shorter runs), and the one that doesn't enforce any MIN_RUN.

    Plots the results in `output/graphs/minrun_impact_comparisons.png`
    """

    results = {}
    for arr_sizes in SIZE_CONFIGURATIONS:
        for arr_size in arr_sizes:
            print(f"Running MIN_RUN benchmark for N={arr_size}")
            # Set the value range to (0, N*100)
            # Not really important as long as the "high" value is reasonably large (=> not too many equal values).
            bounds = (0, arr_size*100)
            sum_with = 0
            for _ in range(N_SAMPLES):
                arr = generate_random_list(arr_size, bounds)
                (_, n_with), _ = run_powersort(arr.copy(), min_run_length=MIN_RUN)
                (_, n_without), _ = run_powersort(arr.copy(), min_run_length=None)
                sum_with += (n_with-n_without)/n_without
            results[arr_size] = (0, sum_with/N_SAMPLES)

    plot_minrun_results(results, "Array size", "# of key comparisons [% diff]",
                        "Performance impact of MIN_RUN and using insertion sort for small runs",
                        "minrun_impact_comparisons", xlog=True)


def benchmark_random() -> None:
    """
    Runs the benchmark for completely random data (random number of runs, random entropy).

    Plots the results in `output/graphs/benchmark_random.png`.
    Saves the raw data in `output/raw_data/benchmark_random.csv`.
    """

    results = {}
    for arr_sizes in SIZE_CONFIGURATIONS:
        for arr_size in arr_sizes:
            print(f"Running RANDOM benchmark for N={arr_size}")
            # Set the value range to (0, N*100)
            # Not really important as long as the "high" value is reasonably large (=> not too many equal values).
            bounds = (0, arr_size*100)
            sum_merge_sort = 0
            sum_natural_merge_sort = 0
            sum_timsort = 0
            sum_powersort = 0
            sum_python_sort = 0
            for _ in range(N_SAMPLES):
                arr = generate_random_list(arr_size, bounds)
                (_, n_merge_sort), _ = run_merge_sort(arr.copy())
                (_, n_natural_merge_sort), _ = run_natural_merge_sort(arr.copy())
                (_, n_timsort), _ = run_timsort(arr.copy())
                (_, n_powersort), _ = run_powersort(arr.copy())
                (_, n_python_sort), _ = run_python_sort_for_comparisons(arr.copy())
                delta = lambda n: (n-n_merge_sort)/n_merge_sort
                sum_merge_sort += delta(n_merge_sort)
                sum_natural_merge_sort += delta(n_natural_merge_sort)
                sum_timsort += delta(n_timsort)
                sum_powersort += delta(n_powersort)
                sum_python_sort += delta(n_python_sort)
            results[arr_size] = (sum_merge_sort/N_SAMPLES,
                                    sum_natural_merge_sort/N_SAMPLES,
                                    sum_timsort/N_SAMPLES,
                                    sum_powersort/N_SAMPLES,
                                    sum_python_sort/N_SAMPLES)
    file_name = "benchmark_random"
    save_to_csv(results, file_name)
    plot_results(results, "Array size (N)", "# of key comparisons [% diff from Merge Sort]",
                 f"Array size vs. # of key comparisons",
                 file_name, fit_to_poly=True, show=False)


def benchmark_runs() -> None:
    """
    Runs the benchmark for data with the predetermined number of runs.
    This number of runs comes from RUNS_CONFIGURATIONS.

    Plots the results in `output/graphs/benchmark_runs_<category>.png`.
    Saves the raw data in `output/raw_data/benchmark_runs_<category>.csv`.
    """

    for config_name, factor in RUNS_CONFIGURATIONS.items():
        _benchmark_runs(config_name, factor)


def _benchmark_runs(config_name: str, factor: int) -> None:
    results = {}
    for arr_sizes in SIZE_CONFIGURATIONS:
        for arr_size in arr_sizes:
            print(f"Running RUNS benchmark ({config_name}) for N={arr_size}")
            # Set the value range to (0, N*100)
            # Not really important as long as the "high" value is reasonably large (=> not too many equal values).
            bounds = (0, arr_size * 100)
            n_runs = arr_size // factor
            if not n_runs:
                continue
            sum_merge_sort = 0
            sum_natural_merge_sort = 0
            sum_timsort = 0
            sum_powersort = 0
            sum_python_sort = 0
            for _ in range(N_SAMPLES):
                arr = generate_random_list(arr_size, bounds, number_of_runs=n_runs)
                (_, n_merge_sort), _ = run_merge_sort(arr.copy())
                (_, n_natural_merge_sort), _ = run_natural_merge_sort(arr.copy())
                (_, n_timsort), _ = run_timsort(arr.copy())
                (_, n_powersort), _ = run_powersort(arr.copy())
                (_, n_python_sort), _ = run_python_sort_for_comparisons(arr.copy())
                delta = lambda n: (n - n_merge_sort) / n_merge_sort
                sum_merge_sort += delta(n_merge_sort)
                sum_natural_merge_sort += delta(n_natural_merge_sort)
                sum_timsort += delta(n_timsort)
                sum_powersort += delta(n_powersort)
                sum_python_sort += delta(n_python_sort)
            results[arr_size] = (sum_merge_sort / N_SAMPLES,
                                 sum_natural_merge_sort / N_SAMPLES,
                                 sum_timsort / N_SAMPLES,
                                 sum_powersort / N_SAMPLES,
                                 sum_python_sort / N_SAMPLES)
    file_name = f"benchmark_runs_{config_name}"
    save_to_csv(results, file_name)
    plot_results(results, "Array size (N)", "# of key comparisons [% diff from Merge Sort]",
                 f"Array size vs. # of key comparisons (number of runs is N/{factor} => array is {config_name})",
                 file_name, fit_to_poly=True, show=False)


def benchmark_entropy() -> None:
    """
    Runs the benchmark for data with the predetermined values of normalized run profile entropy.
    This number of runs comes from ENTROPY_CONFIGURATIONS.

    Plots the results in `output/graphs/benchmark_entropy_<category>.png`.
    Saves the raw data in `output/raw_data/benchmark_entropy_<category>.csv`.
    """

    for config_name, entropy_interval in ENTROPY_CONFIGURATIONS.items():
        _benchmark_entropy(config_name, entropy_interval)


def _benchmark_entropy(config_name: str, entropy_interval: Tuple[float, float]) -> None:
    entropy_from, entropy_to = entropy_interval
    results = {}
    for arr_sizes in SIZE_CONFIGURATIONS:
        for arr_size in arr_sizes:
            print(f"Running ENTROPY benchmark ({config_name}) for N={arr_size}")
            # Set the value range to (0, N*100)
            # Not really important as long as the "high" value is reasonably large (=> not too many equal values).
            bounds = (0, arr_size * 100)
            sum_merge_sort = 0
            sum_natural_merge_sort = 0
            sum_timsort = 0
            sum_powersort = 0
            sum_python_sort = 0
            for _ in range(N_SAMPLES):
                arr = generate_random_list(arr_size, bounds, entropy_range=(entropy_from, entropy_to))
                (_, n_merge_sort), _ = run_merge_sort(arr.copy())
                (_, n_natural_merge_sort), _ = run_natural_merge_sort(arr.copy())
                (_, n_timsort), _ = run_timsort(arr.copy())
                (_, n_powersort), _ = run_powersort(arr.copy())
                (_, n_python_sort), _ = run_python_sort_for_comparisons(arr.copy())
                delta = lambda n: (n - n_merge_sort) / n_merge_sort
                sum_merge_sort += delta(n_merge_sort)
                sum_natural_merge_sort += delta(n_natural_merge_sort)
                sum_timsort += delta(n_timsort)
                sum_powersort += delta(n_powersort)
                sum_python_sort += delta(n_python_sort)
            results[arr_size] = (sum_merge_sort / N_SAMPLES,
                                 sum_natural_merge_sort / N_SAMPLES,
                                 sum_timsort / N_SAMPLES,
                                 sum_powersort / N_SAMPLES,
                                 sum_python_sort / N_SAMPLES)
    file_name = f"benchmark_entropy_{config_name}"
    save_to_csv(results, file_name)
    plot_results(results, "Array size (N)", "# of key comparisons [% diff from Merge Sort]",
                 f"Array size vs. # of key comparisons (entropy interval is "
                 f"{entropy_interval[0]*100}%-{entropy_interval[1]*100}% => run profile is {config_name})",
                 file_name, fit_to_poly=True, show=False)


def run_all_benchmarks() -> None:
    """
    Executes all the benchmarks with all the input configurations defined in `config.py`.
    Note: This might take a very long time (hours), depending on the configured settings.
    """
    # benchmark_minrun_impact()
    # benchmark_random()
    benchmark_runs()
    # benchmark_entropy()


if __name__ == '__main__':
    run_all_benchmarks()
