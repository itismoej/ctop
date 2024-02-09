import pytest
import pandas as pd
from quantcast_cli.filters import calc_session_counts


@pytest.fixture
def sample_df():
    return pd.DataFrame(
        {
            "cookie": ["cookie1", "cookie1", "cookie2"],
            "timestamp": [
                "2023-01-01T23:30:00+00:00",
                "2023-01-01T23:30:00+00:00",
                "2023-01-01T23:30:00+00:00",
            ],
        }
    )


def test_with_invalid_date_format(sample_df):
    with pytest.raises(ValueError):
        calc_session_counts("2023/01/01", sample_df)


def test_with_date_having_no_data(sample_df):
    result = calc_session_counts("2023-02-01", sample_df)
    assert result.empty


def test_with_valid_single_date(sample_df):
    result = calc_session_counts("2023-01-01", sample_df)
    expected = pd.Series([2, 1], index=["cookie1", "cookie2"])
    pd.testing.assert_series_equal(result, expected, check_names=False)
