"""
Configurations for the input data to run the benchmarks on.
Configurable properties: input size, number of datapoints for each size, number of runs, entropy of the run profile.

Tuning remarks:
- For more precise results, increase `N_SAMPLES`. However, this proportionally increases
 the running time of the benchmarks.
- For the entropy benchmarks, it is advisable to omit too short (e.g., < 10^3) arrays in the
 `SIZE_CONFIGURATIONS`, as the results generated on them are more noisy.
- For the entropy benchmarks, random input generation takes longer time. For quicker execution,
  consider omitting too long (e.g., >> 10^5) arrays in the `SIZE_CONFIGURATIONS`.
"""

# The number of inputs/datapoints for each input size
N_SAMPLES = 10

"""
Configures what input sizes should be considered for the benchmark inputs.
This values represent the X axis in the plots.
"""
SIZE_CONFIGURATIONS = [
    # [n for n in range(100, 1000, 100)],
    [n for n in range(1000, 10_000, 1000)],
    [n for n in range(10_000, 100_000, 10_000)],
    [n for n in range(100_000, 1_000_001, 100_000)]
]

"""
Configures what number of runs (K) should the generated benchmark inputs have.
The values in this dictionary represent the average run length.
A separate plot is generated for each of the categories.
"""
RUNS_CONFIGURATIONS = {
    "random": 2,               # N/2 runs
    "presorted": 50,           # N/50 runs
    "heavily_presorted": 500,  # N/500 runs
}

"""
Configures what normalized entropy (h(P)) should the run profiles of the generated inputs have.
The values in this dictionary represent the acceptable range for the normalized entropy.
A separate plot is generated for each of the categories.
"""
ENTROPY_CONFIGURATIONS = {
    "very_skewed": (.1, .2),        # 10-20% of log(K)
    "partially_uniform": (.4, .6),  # 40-60% of log(K)
    "heavily_uniform": (.9, 1.),    # 90-100% of log(K)
}

# Minimum run length constant for Timsort and Powersort
MIN_RUN = 32

# Initial threshold to trigger the galloping mode (7 is standard and used in CPython)
INITIAL_GALLOPING_THRESHOLD = 7
