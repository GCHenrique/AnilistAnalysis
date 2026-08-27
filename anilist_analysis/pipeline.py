from . import api
from . import clean
from . import stats
from . import plots

import sys


def run_user_summary(media_type: str, username: str) -> str:

    print_lines = []

    print_lines.append(f"\n==================={media_type.upper()}===================")
    df = api.fetch_user_data(username, media_type)

    print("\nCleaning data...")

    df_no_duplicates = clean.remove_duplicates(df)
    df_no_zeroed_scores = clean.get_only_with_scores(df_no_duplicates)

    status_types = list(set(df["status"]))
    total_media = len(df_no_duplicates)

    for i in status_types:
        qtt_media = len(df_no_duplicates[df_no_duplicates["status"] == i])
        print_lines.append(
            f"\nNumber of {i.lower()} {media_type}: {qtt_media} ({qtt_media * 100 / total_media:.2f}%)"
        )  # Number of each status anime
        df_type = df_no_zeroed_scores[df_no_zeroed_scores["status"] == i]

        score_basics = stats.get_score_basics(df_type)
        if score_basics:
            print_lines.append(
                f"|Mean score: {score_basics[1]:.2f}"
            )  # mean score of each anime status
            print_lines.append(
                f"|Standard Deviation: {score_basics[0]:.2f}"
            )  # variance of each anime scores
            print_lines.append(
                f"|Median score: {score_basics[2]:.2f}"
            )  # median score of each anime status
        else:
            print_lines.append("|No scores to analyze")

    print_lines.append("------------------------------------------------------")

    # Highest score anime and highest score
    maximum_score, maximum_score_media = stats.get_maximum_media(df_no_zeroed_scores)
    print_lines.append(
        f"\n{media_type.capitalize()} with the highest score ({maximum_score}):"
    )
    for media in maximum_score_media:
        print_lines.append("-" + media)

    # Lowest score anime and lowest score
    minimum_score, minimum_score_media = stats.get_minimum_media(df_no_zeroed_scores)
    print_lines.append(
        f"\n{media_type.capitalize()} with the lowest score ({minimum_score}):"
    )
    for media in minimum_score_media:
        print_lines.append("-" + media)

    # Estudio mais visto (deixar para depois, muito difícil)
    # Associacao nota/numero episodios (com grafico)
    # Country of origin count
    # Anime in watching mean progress (in %)
    # Total number of episodes
    return "\n".join(print_lines)


def run_comparison_2(media_type: str, username1: str, username2: str):

    df1 = api.fetch_user_data(username1, media_type)
    df2 = api.fetch_user_data(username2, media_type)

    print("\nCleaning data...")

    df1_completed = clean.get_completed(df1)
    df2_completed = clean.get_completed(df2)

    df1_filtered = clean.get_only_with_scores(df1_completed)
    df2_filtered = clean.get_only_with_scores(df2_completed)

    del df1_completed, df2_completed  # freeing space in memory

    df1_filtered, df2_filtered = clean.get_both_list_same_animes(
        df1_filtered, df2_filtered
    )

    if df1_filtered.empty:
        print(f"There are no {media_type} in common")
        sys.exit(0)

    print(f"\n{len(df1_filtered)} {media_type} in common found")

    df1_filtered_scores = df1_filtered["score"].to_numpy()
    df2_filtered_scores = df2_filtered["score"].to_numpy()

    del df1_filtered, df2_filtered  # again freeing space in memory

    df1_filtered_scores = stats.normalize_to_Z(df1_filtered_scores)
    df2_filtered_scores = stats.normalize_to_Z(df2_filtered_scores)

    plots.comparison_2_plot_creation(
        df1_filtered_scores, df2_filtered_scores, username1, username2, media_type
    )


def save_text_results(argument: str, filename: str):
    print("\nSaving result to text file")
    with open(filename, "w") as f:
        f.write(argument)
