import requests
from pytz import timezone
import datetime


def load_attempts():
    pages = requests.get(
        "https://devman.org/api/challenges/solution_attempts/?page=1").json()["number_of_pages"]
    for page in range(1, pages):
        page_content = requests.get("https://devman.org/api/challenges/solution_attempts/?page={}".format(page))
        for attempt in page_content.json()["records"]:
            yield attempt


def get_midnighters(attempt):
    attempt_date = datetime.datetime.fromtimestamp(attempt["timestamp"])  # .strftime('%Y-%m-%d %H:%M:%S')
    user_timezone = timezone(attempt["timezone"])
    local_time_attempt = user_timezone.localize(attempt_date)
    attempt_time = datetime.datetime.time(local_time_attempt)
    midhight = datetime.datetime.min.time()
    morning = datetime.time(6, 0, 0)
    if midhight < attempt_time < morning:
        print("{} - {}".format(attempt["username"], attempt_time))


if __name__ == "__main__":
    for attempt in load_attempts():
        get_midnighters(attempt)
