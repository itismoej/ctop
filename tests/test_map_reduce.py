import pandas as pd
import pytest

from quantcast_cli.filters import map_reduce


def test_map_reduce_empty_iterable():
    result = map_reduce(lambda x: x, [])
    assert result is None


def _map_reduce_sum_func(series: pd.Series):
    return series.sum()


def test_reduce_sum_func():
    assert _map_reduce_sum_func(pd.Series([1, 2, 3])) == 6


def test_map_reduce_single_chunk():
    chunks = [pd.Series([1, 2, 3])]
    result = map_reduce(_map_reduce_sum_func, chunks)
    assert result == 6


def test_map_reduce_multiple_chunks():
    chunks = [pd.Series([1, 2, 3]), pd.Series([4, 5, 6]), pd.Series([7, 8, 9])]
    result = map_reduce(_map_reduce_sum_func, chunks)
    assert result == 45


def _map_reduce_func_that_raises(*args, **kwargs):
    raise ValueError("An error occurred")


def test_map_reduce_exception_raiser_function():
    with pytest.raises(ValueError):
        _map_reduce_func_that_raises()
    with pytest.raises(ValueError):
        _map_reduce_func_that_raises(1, 2, 3, a="s")


def test_map_reduce_function_raises_exception():
    chunks = [pd.Series([1]), pd.Series([2])]
    with pytest.raises(ValueError):
        map_reduce(_map_reduce_func_that_raises, chunks)
