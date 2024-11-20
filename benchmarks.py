import random
import time

from benchmark_versions.benchmark_merge_sort import merge_sort
from benchmark_versions.benchmark_natural_merge_sort import natural_merge_sort
from benchmark_versions.benchmark_timsort import timsort
from benchmark_versions.benchmark_powersort import powersort

from output_generation import plot_results, plot_minrun_results, save_to_csv
from random_input_generators import generate_random_list


def timeit(func):
    def wrapper(*args, **kwargs):
        start_time = time.process_time()
        result = func(*args, **kwargs)
        time_taken = time.process_time() - start_time
        return result, time_taken * 1000
    return wrapper


class Comparable:
    # Static variable to track the number of comparisons
    comparison_count = 0

    def __init__(self, value):
        self.value = value

    def __lt__(self, other):
        Comparable.comparison_count += 1
        return self.value < other.value

    def __le__(self, other):
        Comparable.comparison_count += 1
        return self.value <= other.value

    def __gt__(self, other):
        Comparable.comparison_count += 1
        return self.value > other.value

    def __ge__(self, other):
        Comparable.comparison_count += 1
        return self.value >= other.value

    def __eq__(self, other):
        Comparable.comparison_count += 1
        return self.value == other.value

    def __ne__(self, other):
        Comparable.comparison_count += 1
        return self.value != other.value


def run_python_sort_for_comparisons(arr):
    Comparable.comparison_count = 0
    wrapped_arr = [Comparable(x) for x in arr]
    sorted(wrapped_arr)
    return Comparable.comparison_count


@timeit
def run_timsort(arr):
    return timsort(arr)


@timeit
def run_powersort(arr, fix_minrun=True):
    return powersort(arr, fix_minrun)


@timeit
def run_natural_merge_sort(arr):
    return natural_merge_sort(arr)


@timeit
def run_merge_sort(arr):
    return merge_sort(arr)


@timeit
def run_python_sort(arr):
    return sorted(arr)


PROD_N_SAMPLES = 10  # TODO more
PROD_SIZE_CONFIGURATIONS = [
    [n for n in range(100, 1000, 100)],
    [n for n in range(1000, 10_000, 1000)],
    [n for n in range(10_000, 100_000, 10_000)],
    [n for n in range(100_000, 1_000_001, 100_000)]
]
PROD_RUNS_CONFIGURATIONS = {
    # TODO explain these values
    # TODO what if I say there will be: N/2 (random), 1000 (presorted), 10 (heavily_presorted) runs?
    "random": 2,
    "presorted": 50,
    "heavily_presorted": 500,
}
PROD_ENTROPY_CONFIGURATIONS = {
    # TODO it's important to understand what distribution does this have, in other to define these categories
    # TODO is this a normal distribution? actually, I think it's converging toward 1.
    "very_skewed": (.1, .2),  # 10-20% of logK
    "partially_uniform": (.4, .6),  # 40-60% of logK
    "heavily_uniform": (.9, 1.),  # 90-100% of logK
}

N_SAMPLES = 10
SIZE_CONFIGURATIONS = [
    # [n for n in range(10, 100, 10)],
    [n for n in range(100, 1000, 100)],
    [n for n in range(1000, 10_000, 1000)],
    [n for n in range(10_000, 100_000, 10_000)],
    # [n for n in range(100_000, 1_000_001, 100_000)]
]
RUNS_CONFIGURATIONS = {
    "random": 2,
    "presorted": 50,
    "heavily_presorted": 500,
}
ENTROPY_CONFIGURATIONS = {
    "very_skewed": (.1, .2),  # 10-20% of logK
    "partially_uniform": (.4, .6),  # 40-60% of logK
    "heavily_uniform": (.9, 1.),  # 90-100% of logK
}


# arr_size vs. comparisons with and without minrun + insertion sorting
def benchmark_minrun_impact():
    results = {}
    for arr_sizes in SIZE_CONFIGURATIONS:
        for arr_size in arr_sizes:
            print(arr_size)
            bounds = (0, arr_size*10)  # TODO?
            sum_with = 0
            for _ in range(N_SAMPLES):
                arr = generate_random_list(arr_size, bounds)
                (_, n_with), _ = run_powersort(arr.copy(), fix_minrun=True)
                (_, n_without), _ = run_powersort(arr.copy(), fix_minrun=False)
                sum_with += (n_with-n_without)/n_without
            results[arr_size] = (0, sum_with/N_SAMPLES)

    plot_minrun_results(results, "Array size", "# of key comparisons [% diff]",
                        "Performance impact of MIN_RUN and using insertion sort for small runs",
                        "minrun_impact_comparisons", xlog=True)
    return results


def benchmark_random():
    results = {}
    for arr_sizes in SIZE_CONFIGURATIONS:
        for arr_size in arr_sizes:
            print(arr_size)
            bounds = (0, arr_size*10)  # TODO?
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
                n_python_sort = run_python_sort_for_comparisons(arr.copy())
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
    return results


def benchmark_runs():
    for config_name, factor in RUNS_CONFIGURATIONS.items():
        _benchmark_runs(config_name, factor)


def _benchmark_runs(config_name, factor):
    results = {}
    for arr_sizes in SIZE_CONFIGURATIONS:
        for arr_size in arr_sizes:
            print(arr_size)
            bounds = (0, arr_size * 10)  # TODO?
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
                n_python_sort = run_python_sort_for_comparisons(arr.copy())
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
    return results


def benchmark_entropy():
    for config_name, entropy_interval in ENTROPY_CONFIGURATIONS.items():
        _benchmark_entropy(config_name, entropy_interval)


def _benchmark_entropy(config_name, entropy_interval):
    """
    TODO the problem is that the algorithms work with a different run profile (because of MIN_RUN=32)
    So results from this might actually be kinda useless, unless the runs are really big?
    => I think this is in fact not a problem, but let's see on results
    """
    entropy_from, entropy_to = entropy_interval
    results = {}
    for arr_sizes in SIZE_CONFIGURATIONS:
        for arr_size in arr_sizes:
            print(arr_size)
            bounds = (0, arr_size * 10)  # TODO?
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
                n_python_sort = run_python_sort_for_comparisons(arr.copy())
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
    return results


def run_all_benchmarks():
    benchmark_minrun_impact()
    # benchmark_random()
    # benchmark_runs()
    # benchmark_entropy()


if __name__ == '__main__':
    run_all_benchmarks()
