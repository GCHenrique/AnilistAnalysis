from anilist_analysis import pipeline
from anilist_analysis.api import AnilistAPIError


def main():
    try:
        pipeline.run_comparison_2()
    except AnilistAPIError as e:
        print(e)


if __name__ == "__main__":
    main()
