import requests
from pytz import timezone
import datetime


def load_attempts(pages):
    for page in range(1, pages):
        attempts = fetch_page_data(
            "https://devman.org/api/challenges/solution_attempts/",
            page=page
        )["records"]
        for attempt in attempts:
            yield attempt


def fetch_page_data(url, **kwargs):
    page_data = requests.get(url, params=kwargs).json()
    return page_data


def get_midnighters(attempt):
    attempt_date = datetime.datetime.fromtimestamp(attempt["timestamp"])
    user_timezone = timezone(attempt["timezone"])
    local_time_attempt = user_timezone.localize(attempt_date)
    attempt_time = datetime.datetime.time(local_time_attempt)
    midhight = datetime.datetime.min.time()
    morning = datetime.time(6, 0, 0)
    if morning > attempt_time > midhight:
        return attempt["username"]


def print_midnighters(midnighters):
    print("These are users with red eyes:")
    for midnighter in midnighters:
        print(midnighter)


if __name__ == "__main__":
    midnighters = set()
    pages_number = fetch_page_data(
        "https://devman.org/api/challenges/solution_attempts/",
        page=1
    )["number_of_pages"]
    for attempt in load_attempts(pages_number):
        midnighter = get_midnighters(attempt)
        if midnighter is not None:
            midnighters.add(midnighter)
    print_midnighters(midnighters)

