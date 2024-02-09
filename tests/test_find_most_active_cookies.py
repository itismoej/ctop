import os
import tempfile
from contextlib import contextmanager

from quantcast_cli.filters import find_most_active_cookies


@contextmanager
def temp_csv_file(data: str):
    """Context manager to create and automatically delete a temporary CSV file."""
    temp_file = tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".csv")
    try:
        temp_file.write(data)
        temp_file.close()
        yield temp_file.name
    finally:
        os.remove(temp_file.name)


# Example test data
test_csv_data = """
cookie,timestamp
cookie1,2018-12-09T14:19:00+00:00
cookie2,2018-12-09T10:13:00+00:00
cookie1,2018-12-08T22:19:00+00:00
"""


def test_find_most_active_cookies_single_most_active():
    with temp_csv_file(test_csv_data) as filename:
        result = find_most_active_cookies("2018-12-09", filename)
        assert result == ["cookie1", "cookie2"]


def test_find_most_active_cookies_empty_file():
    with temp_csv_file("") as filename:
        result = find_most_active_cookies("2018-12-09", filename)
        assert result == []


def test_find_most_active_cookies_non_existent_date():
    with temp_csv_file(test_csv_data) as filename:
        result = find_most_active_cookies("2018-12-10", filename)
        assert result == []


def test_find_most_active_cookies_multiple_most_active():
    data = """
cookie,timestamp
cookie1,2018-12-09T14:19:00+00:00
cookie2,2018-12-09T10:13:00+00:00
cookie3,2018-12-09T12:14:00+00:00
cookie1,2018-12-09T09:19:00+00:00
cookie2,2018-12-09T17:00:00+00:00
"""
    with temp_csv_file(data) as filename:
        result = find_most_active_cookies("2018-12-09", filename)
        assert sorted(result) == ["cookie1", "cookie2"]


def test_find_most_active_cookies_with_different_chunk_sizes():
    data = """
cookie,timestamp
cookie1,2018-12-09T14:19:00+00:00
cookie2,2018-12-09T10:13:00+00:00
cookie3,2018-12-09T12:14:00+00:00
cookie1,2018-12-09T09:19:00+00:00
cookie2,2018-12-09T17:00:00+00:00
"""
    with temp_csv_file(data) as filename:
        result_small_chunk = find_most_active_cookies(
            "2018-12-09", filename, chunk_size=2
        )
        result_large_chunk = find_most_active_cookies(
            "2018-12-09", filename, chunk_size=10**6
        )
        assert sorted(result_small_chunk) == sorted(result_large_chunk)
