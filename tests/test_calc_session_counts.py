import pytest
from quantcast_cli.filters import calc_session_counts


@pytest.fixture
def sample_data():
    return [
        {"cookie": "cookie1", "timestamp": "2018-12-01T23:30:00+00:00"},
        {"cookie": "cookie2", "timestamp": "2018-12-01T12:24:00+00:00"},
        {"cookie": "cookie1", "timestamp": "2018-12-02T11:21:00+00:00"},
        {"cookie": "cookie3", "timestamp": "2018-12-02T15:45:00+00:00"},
    ]


def test_with_date_having_no_data():
    result = calc_session_counts([])
    assert result == {}  # Expect an empty dictionary for no data


def test_calc_session_counts_with_multiple_dates(sample_data):
    result = calc_session_counts(sample_data)
    expected = {"cookie1": 2, "cookie2": 1, "cookie3": 1}
    assert result == expected
