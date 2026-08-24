import numpy as np


def normalize_to_Z(np_list: np.ndarray):
    try:
        np_list = (np_list - np_list.mean()) / np_list.std(ddof=0)

    except ZeroDivisionError:
        np_list = np_list - np_list.mean()

    return np_list


def get_correlations(
    array1: np.ndarray, array2: np.ndarray
) -> tuple[float, np.ndarray, np.ndarray]:
    corr = np.corrcoef(array1, array2)[0, 1]
    beta, alpha = np.polyfit(array1, array2, 1)
    x = np.linspace(array1.min(), array1.max(), 100)
    y = alpha + beta * x

    print(f"Correlation found: {corr: .4f}")

    return corr, x, y
