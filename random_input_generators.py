from typing import Tuple, List, Generator

import numpy as np
import random


# TODO move to utils?
def _calc_entropy(run_profile: List[int]) -> float:
    arr = np.array(run_profile) / sum(run_profile)
    return -np.sum(arr * np.log2(arr))


def _calc_entropy_bounds(arr_len: int, arr_sum: int) -> Tuple[float, float]:
    # max entropy is log(k) by definition, where k is number of runs
    max_entropy = np.log2(arr_len)  # FIXME take remainder into account
    # min entropy is when the profile is most skewed, like this [2,2,...,2,2,X] where X is the remainder
    # note that min run size is 2
    x = arr_sum - 2*(arr_len-1)  # value of X (remainder)
    n2 = 2 / arr_sum  # normalized value of 2
    nx = x / arr_sum  # normalized value of X
    e2 = -n2 * np.log2(n2)  # entropy "contribution" of a single 2
    ex = -nx * np.log2(nx)  # entropy "contribution" of X
    min_entropy = ex + e2*(arr_len-1)
    return min_entropy, max_entropy


def generate_random_list(n: int, bounds: Tuple[int, int], number_of_runs: int | None = None,
                         entropy_range: Tuple[float, float] | None = None) -> List[int]:
    # TODO docstring
    if number_of_runs or entropy_range:
        # Get run profile (random array [1..n_runs] summing to <size>)
        if number_of_runs:
            prof = _generate_random_run_profile(n, number_of_runs)
        else:
            # TODO move to separate function
            profiles = []
            # it could happen that we don't find run with desired entropy => try different n_runs
            while not profiles:
                # TODO avg run size is 4 with this, change to //32 ? Do this, this might change the results A LOT
                n_runs = random.randint(2, n // 2)
                min_entropy, max_entropy = _calc_entropy_bounds(n_runs, n)
                # TODO add option to iterate from other direction too? for faster execution
                for profile in _generate_profiles_with_increasing_entropy(n, n_runs):
                    entropy = round(_calc_entropy(profile), 4)
                    entropy_factor = (entropy - min_entropy) / (max_entropy - min_entropy)  # TODO rename *factor*
                    if entropy_range[0] <= entropy_factor <= entropy_range[1]:
                        profiles.append(profile)
                    elif profiles:
                        break
            prof = random.choice(profiles)
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


def _generate_random_run_profile(n: int, q: int) -> List[int]:
    runs = [2] * q  # minimal size of a run is 2
    for _ in range(n-q*2):
        i = random.randint(0, q-1)
        runs[i] += 1
    return runs


def _generate_random_run(n: int, bounds: Tuple[int, int],
                         first_bounds: Tuple[int, int]) -> Tuple[List[int], bool]:
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
    return [first] + rest, bool(increasing)


def _generate_profiles_with_increasing_entropy(arr_size: int, n_runs: int) -> Generator:
    # The idea is to generate run profiles with increasing entropy
    # Start with almost sorted array, and gradually balance it
    prof = [2] * (n_runs-1) + [arr_size-2*(n_runs-1)]
    yield prof
    i = 0
    while prof[i] < prof[-1]:
        prof[i] += 1
        prof[-1] -= 1
        yield prof
        i = (i+1) % (n_runs-1)
