import pandas as pd
import pytest

from quantcast_cli.search import find_first_occurrence, notfound


@pytest.fixture
def sample_df():
    data = {
        "cookies": ["a", "a", "a", "a", "a"],
        "timestamp": [
            "2018-12-09T23:30:00+00:00",
            "2018-12-08T23:30:00+00:00",
            "2018-12-08T23:20:00+00:00",
            "2018-12-08T23:10:00+00:00",
            "2018-12-07T23:30:00+00:00",
        ],
    }
    return pd.DataFrame(data)


def test_empty_dataframe():
    df = pd.DataFrame({"timestamp": [], "cookies": []})
    assert find_first_occurrence("2021-01-01", df) is notfound


def test_date_not_exist(sample_df):
    assert find_first_occurrence("2002-01-01", sample_df) is notfound


def test_multiple_occurrences_first_index_returned(sample_df):
    assert find_first_occurrence("2018-12-08", sample_df) == 1


def test_date_is_first_row(sample_df):
    assert find_first_occurrence("2018-12-09", sample_df) == 0


def test_date_is_last_row(sample_df):
    assert find_first_occurrence("2018-12-07", sample_df) == 4
