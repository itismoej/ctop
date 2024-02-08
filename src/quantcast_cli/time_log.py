import time
from contextlib import contextmanager


@contextmanager
def time_log(name: str = "Elapsed Time"):
    start_time = time.time()
    try:
        yield
    finally:
        print(f"{name}: {time.time() - start_time:.2f} secs")
