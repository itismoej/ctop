import pytest
from quantcast_cli.filters import map_reduce, calc_session_counts


@pytest.fixture
def data():
    return [
        {"cookie": "cookie1", "timestamp": "2023-01-01T23:30:00+00:00"},
        {"cookie": "cookie1", "timestamp": "2023-01-01T23:30:00+00:00"},
        {"cookie": "cookie2", "timestamp": "2023-01-01T23:30:00+00:00"},
        {"cookie": "cookie1", "timestamp": "2023-01-01T23:30:00+00:00"},
        {"cookie": "cookie3", "timestamp": "2023-01-01T23:30:00+00:00"},
    ]


def test_map_reduce_empty_iterable():
    result = map_reduce(lambda x: x, [])
    assert result is None


def test_map_reduce(data):
    result = map_reduce(calc_session_counts, data)
    expected = {"cookie1": 3, "cookie2": 1, "cookie3": 1}
    assert result == expected
