import pandas as pd

notfound = object()
DATE_OFFSET = 10  # offset index for extracting date => "YYYY-MM-DD..."[:10]


def get_date(df, index, date_offset: int = DATE_OFFSET):
    return df.iloc[index].timestamp[:date_offset]


def get_adjacent(df, index, find_last: bool = False):
    start, end = 0, len(df) - 1

    if find_last and index < end:
        return get_date(df, index + 1)
    elif not find_last and index > start:
        return get_date(df, index - 1)

    return notfound


def df_binary_search(desired_date: str, df: pd.DataFrame, find_last: bool = False):
    if df.empty:
        return notfound

    start, end = 0, len(df) - 1
    left, right = (start, end)
    while right >= left:
        mid = (left + right) // 2
        current = df.iloc[mid].timestamp[:DATE_OFFSET]
        adjacent = get_adjacent(df, mid, find_last=find_last)
        is_the_same = adjacent == current == desired_date
        if current < desired_date or (not find_last and is_the_same):
            right = mid - 1
        elif current > desired_date or (find_last and is_the_same):
            left = mid + 1
        else:
            return mid

    return notfound


def find_first_occurrence(desired_date: str, df: pd.DataFrame):
    return df_binary_search(desired_date, df)


def find_last_occurrence(desired_date: str, df: pd.DataFrame):
    return df_binary_search(desired_date, df, find_last=True)
