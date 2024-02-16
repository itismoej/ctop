import csv
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime
from functools import reduce
from pathlib import Path
from typing import Union

from .search import find_first_occurrence, find_last_occurrence, notfound
from .utils import reducer_for_dict as _default_reducer_for_dict


def filter_by_date(date: str, data: list[dict]):
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise ValueError(
            f"The date '{date}' does not match the ISO 8601 format 'YYYY-MM-DD'."
        )

    _from = find_first_occurrence(date, data)
    _to = find_last_occurrence(date, data)
    if _from is notfound or _to is notfound:
        return []

    filtered_data = data[_from : _to + 1]
    return filtered_data


def calc_session_counts(data: list[dict]):
    counts = defaultdict(int)
    for row in data:
        cookie = row["cookie"]
        counts[cookie] += 1
    return counts


def chunk_iterable_generator(iterable, chunk_size: int = 10**6):
    for i in range(0, len(iterable), chunk_size):
        yield iterable[i : i + chunk_size]


def map_reduce(func, iterable, reducer=_default_reducer_for_dict):
    chunks = chunk_iterable_generator(iterable)
    with ProcessPoolExecutor() as executor:
        results = [executor.submit(func, chunk) for chunk in chunks]
    if not results:
        return None
    retrieved_results = map(lambda x: x.result(), results)
    reduced_result = reduce(reducer, retrieved_results)
    return reduced_result


def read_csv(file_path):
    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return [row for row in reader]


def find_most_active_cookies(date: str, file: Union[Path, str]):
    data = filter_by_date(date, read_csv(file))
    counts = map_reduce(calc_session_counts, data)
    if not counts:
        return []
    max_count = max(counts.values())
    most_active_cookies = [
        cookie for cookie, count in counts.items() if count == max_count
    ]
    return most_active_cookies
