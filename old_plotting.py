import matplotlib.pyplot as plt
import numpy as np


def plot_minrun_results(data, x_label, y_label, title, file_name):
    x = list(data.keys())
    data_powersort_without_insertion_sort = [v[0] for v in data.values()]
    data_powersort_with_insertion_sort = [v[1] for v in data.values()]

    try:
        poly_without = np.poly1d(np.polyfit(x, data_powersort_without_insertion_sort, 5))
        poly_with = np.poly1d(np.polyfit(x, data_powersort_with_insertion_sort, 5))
    except np.RankWarning:
        pass

    plt.figure(figsize=(10, 6))
    plt.plot(x, data_powersort_without_insertion_sort,
             label='Powersort without MIN_RUN', color='orange', alpha=0.2)
    plt.plot(x, data_powersort_with_insertion_sort,
             label='Powersort with MIN_RUN=32', color='cyan', alpha=0.2)

    plt.plot(x, poly_without(x), color='orange', linewidth=3)
    plt.plot(x, poly_with(x), color='cyan', linewidth=3)

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.legend()
    plt.savefig(f'./graphs/{file_name}.png')


def plot_results(data, x_label, y_label, title, file_name, fit_to_poly=True):
    x = list(data.keys())
    data_merge_sort = [v[0] for v in data.values()]
    data_natural_merge_sort = [v[1] for v in data.values()]
    data_timsort = [v[2] for v in data.values()]
    data_powersort = [v[3] for v in data.values()]
    data_python_sort = [v[4] for v in data.values()]

    if fit_to_poly:
        try:
            poly_merge_sort = np.poly1d(np.polyfit(x, data_merge_sort, 5))
            poly_natural_merge_sort = np.poly1d(np.polyfit(x, data_natural_merge_sort, 5))
            poly_timsort = np.poly1d(np.polyfit(x, data_timsort, 5))
            poly_powersort = np.poly1d(np.polyfit(x, data_powersort, 5))
            poly_python_sort = np.poly1d(np.polyfit(x, data_python_sort, 5))
        except np.RankWarning:
            pass

    plt.figure(figsize=(10, 6))
    alpha = 0.2 if fit_to_poly else 1
    plt.plot(x, data_merge_sort, color='cyan', alpha=alpha)
    plt.plot(x, data_natural_merge_sort, color='blue', alpha=alpha)
    plt.plot(x, data_timsort, color='green', alpha=alpha)
    plt.plot(x, data_powersort, color='orange', alpha=alpha)
    plt.plot(x, data_python_sort, color='red', alpha=alpha-0.1)

    if fit_to_poly:
        plt.plot(x, poly_merge_sort(x), label='Merge Sort', color='cyan', linewidth=3)
        plt.plot(x, poly_natural_merge_sort(x), label='Natural Merge Sort', color='blue', linewidth=3)
        plt.plot(x, poly_timsort(x), label='Timsort', color='green', linewidth=3)
        plt.plot(x, poly_powersort(x), label='Powersort', color='orange', linewidth=3)
        plt.plot(x, poly_python_sort(x), label='Python sort()', color='red', linewidth=3)

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.legend()
    plt.savefig(f'./graphs/{file_name}.png')
