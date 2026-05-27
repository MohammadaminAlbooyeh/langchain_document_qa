import pytest
import time


def test_response_time():
    start = time.time()
    time.sleep(0.1)
    elapsed = time.time() - start
    assert elapsed < 1.0
