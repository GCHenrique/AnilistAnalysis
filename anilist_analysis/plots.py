import matplotlib.pyplot as plt
import numpy as np
from . import stats


def plot_creation(list1: np.ndarray, list2: np.ndarray):
    plt.scatter(
        list1,
        list2,
        marker=".",
        color="red",
        label="Z corrected data points",
    )

    corr, x, y = stats.get_correlations(list1, list2)

    plt.plot(x, y, "-", color="blue", label=f"Correlation: {corr:.4f}")
    plt.legend()

    plt.grid(alpha=0.2)

    plt.show()
