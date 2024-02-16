import pytest
from datetime import datetime
from quantcast_cli.filters import filter_by_date


@pytest.fixture
def sample_data():
    data = [
        {"timestamp": "2018-12-04T23:30:00+00:00", "cookie": "e"},
        {"timestamp": "2018-12-03T23:30:00+00:00", "cookie": "d"},
        {"timestamp": "2018-12-02T23:30:00+00:00", "cookie": "c"},
        {"timestamp": "2018-12-02T23:30:00+00:00", "cookie": "b"},
        {"timestamp": "2018-12-01T23:30:00+00:00", "cookie": "a"},
    ]
    return data


def test_filter_by_date_empty_return(sample_data):
    result_data = filter_by_date("2018-12-05", sample_data)
    assert not result_data  # Empty list is returned for no matches.


def test_filter_by_date_single_occurrence(sample_data):
    result_data = filter_by_date("2018-12-01", sample_data)
    assert len(result_data) == 1
    assert result_data[0]["timestamp"].startswith("2018-12-01")


def test_filter_by_date_multiple_occurrences(sample_data):
    result_data = filter_by_date("2018-12-02", sample_data)
    assert len(result_data) == 2
    assert all(item["timestamp"].startswith("2018-12-02") for item in result_data)


def test_filter_by_date_with_invalid_date_format(sample_data):
    with pytest.raises(ValueError):
        filter_by_date("invalid-date", sample_data)
