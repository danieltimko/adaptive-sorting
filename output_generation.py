from typing import Dict, Tuple
import csv

from matplotlib.ticker import PercentFormatter
import matplotlib.pyplot as plt
import numpy as np

from config import MIN_RUN

"""
Type alias for the benchmark results
{array size: (results_ms, results_nms, results_timsort, results_powersort, results_python_sort)}
Results values are relative difference [%] from the baseline (mergesort). Therefore, results_ms is always 0.0.
"""
TResults = Dict[int, Tuple[float, float, float, float, float]]

CSV_DELIMITER = ','


def save_to_csv(results: TResults, file_name: str) -> None:
    """
    Saves the benchmark results as a CSV file in the output directory.

    :param results: Benchmark results
    :param file_name: Name of the output CSV file
    :return: None; Side effect: CSV file with the results
    """

    with open(f'./output/raw_data/{file_name}.csv', mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=CSV_DELIMITER)
        # First line is header
        writer.writerow(['Array size [-]',
                         'Merge Sort [%]',
                         'Natural Merge Sort [%]',
                         'Timsort [%]',
                         'Powersort [%]',
                         'Python .sort() [%]',
                         # TODO add number of samples/datapoints?
                         # TODO or add all datapoints to csv, before aggregating them
                         ])
        for arr_size, data in results.items():
            writer.writerow([arr_size, *data])


def plot_minrun_results(data: Dict[int, Tuple[int, float]], x_label: str, y_label: str,
                        title: str, file_name: str, xlog: bool = False, show: bool = False) -> None:
    """
    Generates a plot visualization for the MIN_RUN benchmark and saves it as a PNG file in the output directory.

    :param data: Benchmark results - {array size: (results_without_minrun, results_with_minrun)}
        Results values are relative difference [%] from the baseline (results_without_minrun).
        Therefore, results_without_minrun is always 0.0.
    :param x_label: Label for the X axis (array size)
    :param y_label: Label for the Y axis (% diff)
    :param title: Title of the plot
    :param file_name: Name of the output PNG file
    :param xlog: Whether to use logarithmic scale for the X axis. Useful when the experiment is performed in such a way
        that the datapoints for lower x values are much denser, and the datapoints for higher x values are more sparse.
    :param show: Whether to show (open) the generated plot; Useful for debugging purposes.
    :return: None; Side effect: PNG file with the generated plot
    """

    plt.figure(figsize=(10, 6))
    x = list(data.keys())
    data_powersort_without_insertion_sort = [v[0] for v in data.values()]
    data_powersort_with_insertion_sort = [v[1] for v in data.values()]

    plt.plot(x, data_powersort_without_insertion_sort, label='Powersort without MIN_RUN', color='orange', linewidth=3)
    plt.plot(x, data_powersort_with_insertion_sort, label=f'Powersort with MIN_RUN={MIN_RUN}', color='cyan', linewidth=3)

    if xlog:
        plt.xscale('log')
    plt.gca().yaxis.set_major_formatter(PercentFormatter(xmax=1))
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.legend()
    plt.savefig(f'./output/graphs/{file_name}.png')
    if show:
        plt.show()


def plot_results(data: TResults, x_label: str, y_label: str, title: str,
                 file_name: str, fit_to_poly: bool = True, show: bool = False) -> None:
    """
    Generates a plot visualization for the benchmark and saves it as a PNG file in the output directory.
    Uses logarithmic scale for the X axis.

    :param data: Benchmark results; See the definition of TResults
    :param x_label: Label for the X axis (array size)
    :param y_label: Label for the Y axis (% diff)
    :param title: Title of the plot
    :param file_name: Name of the output PNG file
    :param fit_to_poly: Whether the result graphs should be fitted to a polynomial (using the least squares fitting).
        If True, the generated plot contains the both layers: the raw results (opaque colors),
        and the smoothed out results (more transparent colors).
    :param show: Whether to show (open) the generated plot; Useful for debugging purposes.
    :return: None; Side effect: PNG file with the generated plot
    """

    plt.figure(figsize=(10, 6))
    x = list(data.keys())
    data_merge_sort = [v[0] for v in data.values()]
    data_natural_merge_sort = [v[1] for v in data.values()]
    data_timsort = [v[2] for v in data.values()]
    data_powersort = [v[3] for v in data.values()]
    data_python_sort = [v[4] for v in data.values()]

    alpha = 0.15 if fit_to_poly else 1
    plt.plot(x, data_merge_sort, color='cyan', alpha=alpha)
    plt.plot(x, data_natural_merge_sort, color='blue', alpha=alpha)
    plt.plot(x, data_timsort, color='green', alpha=alpha)
    plt.plot(x, data_powersort, color='orange', alpha=alpha)
    plt.plot(x, data_python_sort, color='red', alpha=alpha-0.1)

    if fit_to_poly:
        try:
            # TODO play with 'deg' parameter; rn plots are too smooth on the first half of X axis (problem with xlog?)
            poly_merge_sort = np.poly1d(np.polyfit(x, data_merge_sort, 5))
            poly_natural_merge_sort = np.poly1d(np.polyfit(x, data_natural_merge_sort, 5))
            poly_timsort = np.poly1d(np.polyfit(x, data_timsort, 5))
            poly_powersort = np.poly1d(np.polyfit(x, data_powersort, 5))
            poly_python_sort = np.poly1d(np.polyfit(x, data_python_sort, 5))
        except np.RankWarning:
            pass
        plt.plot(x, poly_merge_sort(x), label='Merge Sort', color='cyan', linewidth=3)
        plt.plot(x, poly_natural_merge_sort(x), label='Natural Merge Sort', color='blue', linewidth=3)
        plt.plot(x, poly_timsort(x), label='Timsort', color='green', linewidth=3)
        plt.plot(x, poly_powersort(x), label='Powersort', color='orange', linewidth=3)
        plt.plot(x, poly_python_sort(x), label='Python .sort()', color='red', linewidth=3)

    plt.xscale('log')
    plt.gca().yaxis.set_major_formatter(PercentFormatter(xmax=1))
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.legend()
    plt.savefig(f'./output/graphs/{file_name}.png')
    if show:
        plt.show()
