from concurrent.futures import ProcessPoolExecutor
from functools import reduce, partial

import pandas as pd


def filter_by_date(date: str, df: pd.DataFrame) -> pd.DataFrame:
    return df[df.timestamp.str.startswith(date)]


def calc_session_counts(date: str, df: pd.DataFrame) -> pd.Series:
    return filter_by_date(date, df).groupby("cookie").size()


def map_reduce(func, iterable):
    with ProcessPoolExecutor() as executor:
        results = [executor.submit(func, chunk) for chunk in iterable]
    if not results:
        return None
    retrieved_results = map(lambda x: x.result(), results)
    reduced_result = reduce(
        lambda acc, prev: acc.add(prev, fill_value=0), retrieved_results
    )
    return reduced_result


def find_most_active_cookies(date: str, file, chunk_size: int = 10**6) -> list[str]:
    chunks = pd.read_csv(file, chunksize=chunk_size)
    counts = map_reduce(partial(calc_session_counts, date), chunks)
    max_count: int = counts.max()
    most_active_cookies_series: pd.Series = counts.loc[counts == max_count]
    most_active_cookies: list[str] = most_active_cookies_series.index.tolist()
    return most_active_cookies
