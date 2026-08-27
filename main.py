from anilist_analysis import pipeline
from anilist_analysis.api import AnilistAPIError, FetchingError
from requests.exceptions import ConnectionError, HTTPError

# Add support to choose type of media
# Add 3. Get inference for whole anilist population (with random id's)


def main():
    while True:
        print("Choose one:\n")
        print("(1). Make an user's summary")
        print("(2). Compare two users\n")
        flag_main = input()

        if flag_main in ("1", "2"):
            break
    try:
        if flag_main == "1":
            username = input("Input username: ")

            string1 = pipeline.run_user_summary('anime', username)
            string2 = pipeline.run_user_summary('manga', username)

            filename = f'results/{username}.txt'
            pipeline.save_text_results(string1 + '\n' + string2, filename)

        elif flag_main == "2":
            username1 = input("Input username: ")
            username2 = input("Input second username: ")
            
            pipeline.run_comparison_2('anime', username1, username2)
            pipeline.run_comparison_2('manga', username1, username2)

    except AnilistAPIError as e:
        print(e)

    except ConnectionError:
        print("Network connection failed")

    except HTTPError as e:
        print(f"HTTP error occurred: {e}")

    except FetchingError as e:
        print(e)


if __name__ == "__main__":
    main()
