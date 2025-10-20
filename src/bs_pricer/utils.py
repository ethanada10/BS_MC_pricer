from contextlib import contextmanager
import time

@contextmanager
def timed():
    t0 = time.perf_counter()
    try:
        yield
    finally:
        t1 = time.perf_counter()
        print(f"[timed] {t1 - t0:.4f}s")
