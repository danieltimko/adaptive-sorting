import numpy as np
import random


# TODO move to utils
def calc_entropy(run_profile):
    arr = np.array(run_profile) / sum(run_profile)
    return -np.sum(arr * np.log2(arr))


def calc_entropy_bounds(arr_len, arr_sum):
    # max entropy is log(k) by definition, where k is number of runs
    max_entropy = np.log2(arr_len)
    # min entropy is when the profile is most skewed, like this [2,2,...,2,2,X] where X is the remainder
    # note that min run size is 2
    x = arr_sum - 2*(arr_len-1)  # value of X (remainder)
    n2 = 2 / arr_sum  # normalized value of 2
    nx = x / arr_sum  # normalized value of X
    e2 = -n2 * np.log2(n2)  # entropy "contribution" of a single 2
    ex = -nx * np.log2(nx)  # entropy "contribution" of X
    min_entropy = ex + e2*(arr_len-1)
    return min_entropy, max_entropy


def generate_random_list(n, bounds, number_of_runs=None, run_profile=None):
    if number_of_runs or run_profile:
        # Get run profile (random array [1..n_runs] summing to <size>)
        if number_of_runs:
            prof = generate_random_run_profile(n, number_of_runs)
        else:
            prof = run_profile
        arr = []
        last_increasing = True
        first_bounds = bounds
        # For each run generate random subarray with constraint on the first element
        for i in range(len(prof)):
            if i != 0:
                if last_increasing:
                    first_bounds = (bounds[0], arr[-1]-1)
                else:
                    first_bounds = (arr[-1]+1, bounds[1])
            run, last_increasing = _generate_random_run(prof[i], bounds, first_bounds)
            arr.extend(run)
        return arr
    return np.random.randint(bounds[0], bounds[1], n).tolist()


def generate_random_run_profile(n, q):
    runs = [2] * q  # minimal size of a run is 2
    for _ in range(n-q*2):
        i = random.randint(0, q-1)
        runs[i] += 1
    return runs


def _generate_random_run(n, bounds, first_bounds):
    first = random.randint(first_bounds[0], first_bounds[1])
    while True:
        increasing = random.randint(0, 1)
        if increasing:
            new_bounds = (first, bounds[1])
        else:
            new_bounds = (bounds[0], first)
        if new_bounds[0] != new_bounds[1]:
            bounds = new_bounds
            break
    while True:
        rest = sorted(np.random.randint(bounds[0], bounds[1]+1, n-1), reverse=not increasing)
        if any(e != first for e in rest):
            break
    return [first] + rest, increasing

