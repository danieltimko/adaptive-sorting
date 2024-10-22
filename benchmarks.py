import time

from benchmark_versions.benchmark_merge_sort import merge_sort
from benchmark_versions.benchmark_natural_merge_sort import natural_merge_sort
from benchmark_versions.benchmark_timsort import timsort
from benchmark_versions.benchmark_powersort import powersort

from plotting import plot_results, plot_minrun_results
from random_input_generators import calc_entropy, generate_random_list


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
def run_powersort(arr, fix_minsize=True):
    return powersort(arr, fix_minsize)


@timeit
def run_natural_merge_sort(arr):
    return natural_merge_sort(arr)


@timeit
def run_merge_sort(arr):
    return merge_sort(arr)


@timeit
def run_python_sort(arr):
    return sorted(arr)


def benchmark_runs_vs_comparisons(reps, arr_size, skip_factor=None, bounds=None):
    if not bounds:
        bounds = (0, arr_size*10)
    results = {}
    for n_runs in range(1, arr_size//2):
        if skip_factor and n_runs % skip_factor != 1:
            continue
        sum_merge_sort = 0
        sum_natural_merge_sort = 0
        sum_timsort = 0
        sum_powersort = 0
        sum_python_sort = 0
        for _ in range(reps):
            arr = generate_random_list(arr_size, bounds, number_of_runs=n_runs)
            (_, n_merge_sort), _ = run_merge_sort(arr.copy())
            (_, n_natural_merge_sort), _ = run_natural_merge_sort(arr.copy())
            (_, n_timsort), _ = run_timsort(arr.copy())
            (_, n_powersort), _ = run_powersort(arr.copy())
            n_python_sort = run_python_sort_for_comparisons(arr.copy())
            sum_merge_sort += n_merge_sort
            sum_natural_merge_sort += n_natural_merge_sort
            sum_timsort += n_timsort
            sum_powersort += n_powersort
            sum_python_sort += n_python_sort
        results[n_runs] = (sum_merge_sort/reps, sum_natural_merge_sort/reps,
                           sum_timsort/reps, sum_powersort/reps, sum_python_sort/reps)
    plot_results(results, "# of runs", "# of key comparisons",
                 f"# of runs vs. # of key comparisons (N = {arr_size})",
                 "runs_vs_comparisons", fit_to_poly=False)
    return results


def benchmark_run_size_vs_cpu_time(reps, arr_size, skip_factor=None, bounds=None):
    if not bounds:
        bounds = (0, arr_size*10)
    results = {}
    for n_runs in range(1, arr_size//2):
        if skip_factor and n_runs % skip_factor != 1:
            continue
        sum_merge_sort = 0
        sum_natural_merge_sort = 0
        sum_timsort = 0
        sum_powersort = 0
        sum_python_sort = 0
        for _ in range(reps):
            arr = generate_random_list(arr_size, bounds, number_of_runs=n_runs)
            _, t_merge_sort = run_merge_sort(arr.copy())
            _, t_natural_merge_sort = run_natural_merge_sort(arr.copy())
            _, t_timsort = run_timsort(arr.copy())
            _, t_powersort = run_powersort(arr.copy())
            _, t_python_sort = run_python_sort(arr.copy())
            sum_merge_sort += t_merge_sort
            sum_natural_merge_sort += t_natural_merge_sort
            sum_timsort += t_timsort
            sum_powersort += t_powersort
            sum_python_sort += t_python_sort
        results[n_runs] = (sum_merge_sort/reps, sum_natural_merge_sort/reps,
                           sum_timsort/reps, sum_powersort/reps, sum_python_sort/reps)
    plot_results(results, "# of runs", "CPU time [ms]",
                 f"# of runs vs. CPU time (N = {arr_size})", "runs_vs_cpu_time")
    return results


def benchmark_entropy_vs_comparisons(reps, arr_size, n_runs, skip_factor=None, bounds=None):
    if not bounds:
        bounds = (0, arr_size*10)
    results = {}
    i = 0
    for prof in _entropy_gen(arr_size, n_runs):
        if skip_factor and i % skip_factor != 0:
            continue
        i += 1
        print(prof[0], prof[-1])
        sum_merge_sort = 0
        sum_natural_merge_sort = 0
        sum_timsort = 0
        sum_powersort = 0
        sum_python_sort = 0
        entropy = round(calc_entropy(prof), 4)
        for _ in range(reps):
            arr = generate_random_list(arr_size, bounds, run_profile=prof)
            (_, n_merge_sort), _ = run_merge_sort(arr.copy())
            (_, n_natural_merge_sort), _ = run_natural_merge_sort(arr.copy())
            (_, n_timsort), _ = run_timsort(arr.copy())
            (_, n_powersort), _ = run_powersort(arr.copy())
            n_python_sort = run_python_sort_for_comparisons(arr.copy())
            sum_merge_sort += n_merge_sort
            sum_natural_merge_sort += n_natural_merge_sort
            sum_timsort += n_timsort
            sum_powersort += n_powersort
            sum_python_sort += n_python_sort
        results[entropy] = (sum_merge_sort/reps, sum_natural_merge_sort/reps,
                            sum_timsort/reps, sum_powersort/reps, sum_python_sort/reps)
    plot_results(results, "Entropy", "# of key comparisons",
                 f"Entropy of the run profile vs. # of key comparisons "
                 f"(N = {arr_size}, # of runs = {n_runs})", "entropy_vs_comparisons")
    return results


def benchmark_entropy_vs_cpu_time(reps, arr_size, n_runs, skip_factor=1, bounds=None):
    if not bounds:
        bounds = (0, arr_size*10)
    results = {}
    i = 0
    for prof in _entropy_gen(arr_size, n_runs):
        if skip_factor and i % skip_factor != 0:
            continue
        i += 1
        sum_merge_sort = 0
        sum_natural_merge_sort = 0
        sum_timsort = 0
        sum_powersort = 0
        sum_python_sort = 0
        entropy = round(calc_entropy(prof), 3)
        for _ in range(reps):
            arr = generate_random_list(arr_size, bounds, run_profile=prof)
            _, t_merge_sort = run_merge_sort(arr.copy())
            _, t_natural_merge_sort = run_natural_merge_sort(arr.copy())
            _, t_timsort = run_timsort(arr.copy())
            _, t_powersort = run_powersort(arr.copy())
            _, t_python_sort = run_python_sort(arr.copy())
            sum_merge_sort += t_merge_sort
            sum_natural_merge_sort += t_natural_merge_sort
            sum_timsort += t_timsort
            sum_powersort += t_powersort
            sum_python_sort += t_python_sort
        results[entropy] = (sum_merge_sort/reps, sum_natural_merge_sort/reps,
                            sum_timsort/reps, sum_powersort/reps, sum_python_sort/reps)
    plot_results(results, "Entropy", "CPU time [ms]",
                 f"Entropy of the run profile vs. CPU time"
                 f"(N = {arr_size}, # of runs = {n_runs})", "entropy_vs_cpu_time")
    return results


# arr_size vs. cpu time with and without minrun + insertion sorting
def benchmark_minrun_impact(min_size, max_size, skip_factor, reps):
    results = {}
    for size in range(min_size, max_size, skip_factor):
        sum_with = 0
        sum_without = 0
        for _ in range(reps):
            arr = generate_random_list(size, (1, size*10))
            inp = arr.copy()
            start_time = time.process_time()
            powersort(inp, fix_minrun=True)
            time_with = time.process_time() - start_time
            inp = arr.copy()
            start_time = time.process_time()
            powersort(inp, fix_minrun=False)
            time_without = time.process_time() - start_time
            sum_with += time_with
            sum_without += time_without
        results[size] = (sum_without / reps, sum_with / reps)
    plot_minrun_results(results, "Array size", "CPU time [s]",
                 f"Impact on performance of MIN_RUN and using insertion sort for small runs",
                 "minrun_impact")
    return results


def _entropy_gen(arr_size, n_runs):
    # The idea is to generate run profiles with increasing entropy
    # Start with almost sorted array, and gradually balance it
    prof = [2] * (n_runs-1) + [arr_size-2*(n_runs-1)]
    i = 0
    while prof[i] < prof[-1]:
        prof[i] += 1
        prof[-1] -= 1
        yield prof
        i += 1
        if i == n_runs-1:
            i = 0


def run_all_benchmarks():
    benchmark_runs_vs_comparisons(1, 100_000, skip_factor=200)
    benchmark_run_size_vs_cpu_time(1, 50_000, skip_factor=100)
    benchmark_entropy_vs_comparisons(1, 1_000, 100)
    benchmark_entropy_vs_cpu_time(4, 50_000, 1000, skip_factor=100)
    benchmark_minrun_impact(100_000, 1_000_000,  10_000, 2)


if __name__ == '__main__':
    run_all_benchmarks()
