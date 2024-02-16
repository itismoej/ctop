import os
from tempfile import NamedTemporaryFile
from contextlib import contextmanager


@contextmanager
def temp_csv_file(data: str):
    """Context manager to create and automatically delete a temporary CSV file."""
    with NamedTemporaryFile(mode="w", suffix=".csv") as temp_file:
        temp_file.write(data)
        temp_file.seek(0)
        yield temp_file
        temp_file.close()


def reducer_for_dict(acc: dict, prev: dict):
    for key in prev:
        if key in acc:
            acc[key] += prev[key]
        else:
            acc[key] = prev[key]
    return acc
