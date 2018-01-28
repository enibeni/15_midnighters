import requests
from pytz import timezone
import datetime


def load_attempts():
    page = 1
    while True:
        page_data = fetch_page_data(
            "https://devman.org/api/challenges/solution_attempts/",
            page=page
        )
        page += 1
        if page_data:
            for attempt in page_data["records"]:
                yield attempt
        else:
            break


def fetch_page_data(url, **kwargs):
    page_data = requests.get(url, params=kwargs)
    if page_data.ok:
        return page_data.json()


def get_midnighter(attempt):
    user_timezone = timezone(attempt["timezone"])
    attempt_date = datetime.datetime.fromtimestamp(
        attempt["timestamp"],
        tz=user_timezone
    )
    midnight_hour = 0
    morning_hour = 6
    if morning_hour > attempt_date.hour > midnight_hour:
        return attempt["username"]


def print_midnighters(midnighters):
    print("These are users with red eyes:")
    for midnighter in midnighters:
        print(midnighter)


if __name__ == "__main__":
    midnighters = set()
    for attempt in load_attempts():
        midnighter = get_midnighter(attempt)
        if midnighter:
            midnighters.add(midnighter)
    print_midnighters(midnighters)

