import pytest

from quantcast_cli.search import find_first_occurrence, notfound


@pytest.fixture
def sample_data():
    data = [
        {"timestamp": "2018-12-09T23:30:00+00:00", "cookie": "a"},
        {"timestamp": "2018-12-08T23:30:00+00:00", "cookie": "a"},
        {"timestamp": "2018-12-08T23:20:00+00:00", "cookie": "a"},
        {"timestamp": "2018-12-08T23:10:00+00:00", "cookie": "a"},
        {"timestamp": "2018-12-07T23:30:00+00:00", "cookie": "a"},
    ]
    return data


def test_empty_data():
    assert find_first_occurrence("2021-12-08", []) is notfound


def test_date_not_exist(sample_data):
    assert find_first_occurrence("2002-01-01", sample_data) is notfound


def test_multiple_occurrences_first_index_returned(sample_data):
    assert find_first_occurrence("2018-12-08", sample_data) == 1


def test_date_is_first_row(sample_data):
    assert find_first_occurrence("2018-12-09", sample_data) == 0


def test_date_is_last_row(sample_data):
    assert find_first_occurrence("2018-12-07", sample_data) == 4
