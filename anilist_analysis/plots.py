import matplotlib.pyplot as plt
import numpy as np

from . import stats


def comparison_2_plot_creation(
    list1: np.ndarray,
    list2: np.ndarray,
    username1: str,
    username2: str,
    media_type: str,
):
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
    plt.title(f"{media_type.capitalize()}")
    plt.xlabel(f"{username2}")
    plt.ylabel(f"{username1}")
    plt.grid(alpha=0.2)

    plt.savefig(f"results/{username1}_{username2}_{media_type}.png")
    plt.close()
