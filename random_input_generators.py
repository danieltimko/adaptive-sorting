from typing import Tuple, List, Generator

import numpy as np
import random


def generate_random_list(n: int, bounds: Tuple[int, int], number_of_runs: int | None = None,
                         entropy_range: Tuple[float, float] | None = None) -> List[int]:
    """
    Generates a random list with the specified properties.

    :param n: Length of the list to generate
    :param bounds: (low, high) Allowed value range for the list's elements
    :param number_of_runs: (optional) Number of runs in the list to generate
    :param entropy_range: (optional) Allowed normalized range for the entropy of the list's run profile
        Normalized entropy is the relative percentual "position" of the (absolute) entropy in the interval bounded
        by the minimal and the maximal possible entropy of run profiles with the same K and N.
        For example, having an entropy value of 4.5, the minimal possible entropy = 1, the maximal possible entropy = 8,
        then the normalized entropy is equal to (4.5-1)/(8-1) = 0.5 (the entropy lies in the middle of the interval).
    :return Randomly generated list with the given properties
    """

    if number_of_runs or entropy_range:
        # Get run profile (random array [1..n_runs] summing to <size>)
        if number_of_runs:
            prof = _generate_random_run_profile(number_of_runs, n)
        else:
            profiles = []
            # it could happen that we don't find run with desired entropy => try different n_runs
            while not profiles:
                # TODO avg run size is 4 with this, change to //32 ? This might change the results
                n_runs = random.randint(2, n // 2)
                min_entropy, max_entropy = _calc_entropy_bounds(n_runs, n)
                # TODO add option to iterate from other direction too? for faster execution of benchmarks
                for profile in _generate_profiles_with_increasing_entropy(n_runs, n):
                    entropy = round(_calc_entropy(profile), 4)
                    normalized_entropy = (entropy - min_entropy) / (max_entropy - min_entropy)
                    if entropy_range[0] <= normalized_entropy <= entropy_range[1]:
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
            run = _generate_random_run(prof[i], bounds, first_bounds)
            last_increasing = run[1] >= run[0]
            arr.extend(run)
        return arr
    return np.random.randint(bounds[0], bounds[1], n).tolist()


def _calc_entropy(run_profile: List[int]) -> float:
    """
    Calculates the entropy of the run profile.

    :param run_profile: Run profile
    :return: Entropy of the run profile
    """

    arr = np.array(run_profile) / sum(run_profile)
    return -np.sum(arr * np.log2(arr))


def _calc_entropy_bounds(k: int, n: int) -> Tuple[float, float]:
    """
    Calculates minimal and maximal possible entropy for run profiles of the specified length and sum.

    :param k: Number of runs (length of the run profile)
    :param n: Total number of input elements (sum of the run profile)
    :return: Minimal and maximal possible entropy
    """

    # max entropy is log(k) by definition, where k is number of runs
    max_entropy = np.log2(k)
    # min entropy is when the profile is most skewed, like this [2,2,...,2,2,X] where X is the remainder
    # note that min run size is 2
    x = n - 2 * (k - 1)  # value of X (remainder)
    n2 = 2 / n  # normalized value of 2
    nx = x / n  # normalized value of X
    e2 = -n2 * np.log2(n2)  # entropy "contribution" of a single 2
    ex = -nx * np.log2(nx)  # entropy "contribution" of X
    min_entropy = ex + e2*(k - 1)
    return min_entropy, max_entropy


def _generate_random_run_profile(k: int, n: int) -> List[int]:
    """
    Generates a random run profile with the specified K and N.

    :param k: Number of runs (length of the run profile)
    :param n: Total number of input elements (sum of the run profile)
    :return: Randomly generated run profile with the given properties
    """

    runs = [2] * k  # minimal size of a run is 2
    for _ in range(n-k*2):
        # assign the element to a random run
        i = random.randint(0, k-1)
        runs[i] += 1
    return runs


def _generate_profiles_with_increasing_entropy(k: int, n: int) -> Generator:
    """
    Generates a finite subset of all possible run profiles with the specified K and N,
    in such a way that each generated run profile has higher entropy than the previous one.

    :param k: Number of runs (length of the run profile)
    :param n: Total number of input elements (sum of the run profile)
    :return: Generator yielding run profiles with the given properties and with the increasing entropy.
    """

    # The idea is to generate run profiles with increasing entropy
    # Start with almost sorted array, and gradually balance it
    prof = [2] * (k-1) + [n-2*(k-1)]
    yield prof
    i = 0
    while prof[i] < prof[-1]:
        prof[i] += 1
        prof[-1] -= 1
        yield prof  # TODO should use .copy() for the final version. Ignore for now to speed up the benchmarks. 
        i = (i+1) % (k-1)


def _generate_random_run(n: int, bounds: Tuple[int, int],
                         first_bounds: Tuple[int, int]) -> List[int]:
    """
    Generates a random run (increasing or decreasing) with the specified length,
    respecting given restrictions for its values.

    :param n: Length of the run
    :param bounds: (low, high) Allowed value range for the run's elements
    :param first_bounds: (low, high) Allowed value range for the first element of the run.
        The first element has to satisfy separate value restrictions in order to interrupt the previous run.
    :return: Randomly generated run
    """

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
    return [first] + rest
