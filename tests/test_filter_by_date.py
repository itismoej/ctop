import pytest
import pandas as pd
from quantcast_cli.filters import filter_by_date


@pytest.fixture
def sample_df():
    data = {
        "timestamp": [
            "2018-12-04T23:30:00+00:00",
            "2018-12-03T23:30:00+00:00",
            "2018-12-02T23:30:00+00:00",
            "2018-12-02T23:30:00+00:00",
            "2018-12-01T23:30:00+00:00",
        ],
        "cookie": ["e", "d", "c", "b", "a"],
    }
    df = pd.DataFrame(data)
    return df


def test_filter_by_date_empty_return(sample_df):
    result_df = filter_by_date("2018-12-05", sample_df)
    assert result_df.empty
    assert set(result_df.columns) == {"timestamp", "cookie"}


def test_filter_by_date_single_occurrence(sample_df):
    result_df = filter_by_date("2018-12-01", sample_df)
    assert len(result_df) == 1
    assert result_df.iloc[0]["timestamp"].startswith("2018-12-01")


def test_filter_by_date_multiple_occurrences(sample_df):
    result_df = filter_by_date("2018-12-02", sample_df)
    assert len(result_df) == 2
    assert all(result_df["timestamp"].str.startswith("2018-12-02"))


def test_filter_by_date_with_invalid_date_format(sample_df):
    with pytest.raises(ValueError):
        filter_by_date("invalid-date", sample_df)
