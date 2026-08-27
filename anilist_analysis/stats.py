import numpy as np
import pandas as pd


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

    print(f"\nCorrelation found: {corr: .4f}")

    return corr, x, y


def get_maximum_media(df: pd.DataFrame) -> tuple[int, list]:
    score = df["score"].max()  # probably 100 but whatever
    media = df[df["score"] == score]["media.title.romaji"].tolist()

    return score, media


def get_minimum_media(df: pd.DataFrame) -> tuple[int, list]:
    score = df["score"].min()

    media = df[df["score"] == score]["media.title.romaji"].tolist()

    return score, media


def get_score_basics(df: pd.DataFrame) -> tuple[float, float, float]:
    if df.empty:
        return None

    mean = df["score"].mean()
    std = df["score"].std(ddof=0)
    median = df["score"].median()

    return std, mean, median
