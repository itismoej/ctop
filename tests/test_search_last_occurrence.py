import pytest

from quantcast_cli.search import find_last_occurrence, notfound


@pytest.fixture
def sample_data():
    return [
        {"timestamp": "2018-12-09T23:30:00+00:00", "cookie": "a"},
        {"timestamp": "2018-12-08T23:30:00+00:00", "cookie": "a"},
        {"timestamp": "2018-12-08T23:20:00+00:00", "cookie": "a"},
        {"timestamp": "2018-12-08T23:10:00+00:00", "cookie": "a"},
        {"timestamp": "2018-12-07T23:30:00+00:00", "cookie": "a"},
    ]


def test_empty_dataframe():
    assert find_last_occurrence("2018-12-08", []) is notfound


def test_date_not_exist(sample_data):
    assert find_last_occurrence("2002-01-01", sample_data) is notfound


def test_multiple_occurrences_last_index_returned(sample_data):
    assert find_last_occurrence("2018-12-08", sample_data) == 3


def test_date_is_first_row(sample_data):
    assert find_last_occurrence("2018-12-09", sample_data) == 0


def test_date_is_last_row(sample_data):
    assert find_last_occurrence("2018-12-07", sample_data) == 4
