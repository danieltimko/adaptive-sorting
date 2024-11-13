from typing import Dict, List, Tuple
import csv

from matplotlib.ticker import PercentFormatter
import matplotlib.pyplot as plt
import numpy as np


TResults = List[Dict[int, Tuple[float, float, float, float, float]]]

CSV_DELIMITER = ','


def save_to_csv(results: TResults, file_name: str) -> None:
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
        for subresults in results:
            for arr_size, data in subresults.items():
                writer.writerow([arr_size, *data])


def plot_minrun_results(results, x_label, y_label, title, file_name):
    plt.figure(figsize=(10, 6))
    for i, data in enumerate(results):
        print(i)
        x = list(data.keys())
        data_powersort_without_insertion_sort = [v[0] for v in data.values()]
        data_powersort_with_insertion_sort = [v[1] for v in data.values()]

        try:
            poly_without = np.poly1d(np.polyfit(x, data_powersort_without_insertion_sort, 5))
            poly_with = np.poly1d(np.polyfit(x, data_powersort_with_insertion_sort, 5))
        except np.RankWarning:
            pass

        plt.plot(x, data_powersort_without_insertion_sort, color='orange', alpha=0.2)
        plt.plot(x, data_powersort_with_insertion_sort, color='cyan', alpha=0.2)

        plt.plot(x, poly_without(x), label='Powersort without MIN_RUN' if i == 0 else '', color='orange', linewidth=3)
        plt.plot(x, poly_with(x), label='Powersort with MIN_RUN=32' if i == 0 else '', color='cyan', linewidth=3)

    plt.xscale('log')
    plt.gca().yaxis.set_major_formatter(PercentFormatter(xmax=1))
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.legend()
    plt.savefig(f'./output/graphs/{file_name}.png')


def plot_results(results, x_label, y_label, title, file_name, fit_to_poly=True, show=False):
    plt.figure(figsize=(10, 6))
    for i, data in enumerate(results):
        if not data:
            continue
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
                poly_merge_sort = np.poly1d(np.polyfit(x, data_merge_sort, 5))
                poly_natural_merge_sort = np.poly1d(np.polyfit(x, data_natural_merge_sort, 5))
                poly_timsort = np.poly1d(np.polyfit(x, data_timsort, 5))
                poly_powersort = np.poly1d(np.polyfit(x, data_powersort, 5))
                poly_python_sort = np.poly1d(np.polyfit(x, data_python_sort, 5))
            except np.RankWarning:
                pass
            plt.plot(x, poly_merge_sort(x), label='Merge Sort' if i == 0 else '', color='cyan', linewidth=3)
            plt.plot(x, poly_natural_merge_sort(x), label='Natural Merge Sort' if i == 0 else '', color='blue', linewidth=3)
            plt.plot(x, poly_timsort(x), label='Timsort' if i == 0 else '', color='green', linewidth=3)
            plt.plot(x, poly_powersort(x), label='Powersort' if i == 0 else '', color='orange', linewidth=3)
            plt.plot(x, poly_python_sort(x), label='Python .sort()' if i == 0 else '', color='red', linewidth=3)

    plt.xscale('log')
    plt.gca().yaxis.set_major_formatter(PercentFormatter(xmax=1))
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.legend()
    plt.savefig(f'./output/graphs/{file_name}.png')
    if show:
        plt.show()
