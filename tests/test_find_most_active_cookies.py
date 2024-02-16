from quantcast_cli.filters import find_most_active_cookies
from quantcast_cli.utils import temp_csv_file

test_csv_data = """cookie,timestamp
cookie1,2018-12-09T14:19:00+00:00
cookie2,2018-12-09T10:13:00+00:00
cookie1,2018-12-08T22:19:00+00:00
"""


def test_find_most_active_cookies_single_most_active():
    with temp_csv_file(test_csv_data) as file:
        result = find_most_active_cookies("2018-12-09", file.name)
        assert result == ["cookie1", "cookie2"]


def test_find_most_active_cookies_empty_file():
    with temp_csv_file("") as file:
        result = find_most_active_cookies("2018-12-09", file.name)
        assert result == []


def test_find_most_active_cookies_non_existent_date():
    with temp_csv_file(test_csv_data) as file:
        result = find_most_active_cookies("2018-12-10", file.name)
        assert result == []


def test_find_most_active_cookies_multiple_most_active():
    data = """cookie,timestamp
cookie1,2018-12-09T14:19:00+00:00
cookie2,2018-12-09T10:13:00+00:00
cookie3,2018-12-09T12:14:00+00:00
cookie1,2018-12-09T09:19:00+00:00
cookie2,2018-12-09T17:00:00+00:00
"""
    with temp_csv_file(data) as file:
        result = find_most_active_cookies("2018-12-09", file.name)
        assert sorted(result) == ["cookie1", "cookie2"]
