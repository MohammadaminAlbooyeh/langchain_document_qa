#!/usr/bin/env python3
import time


def benchmark():
    start = time.time()
    time.sleep(0.5)
    elapsed = time.time() - start
    print(f"Benchmark completed in {elapsed:.2f}s")


if __name__ == "__main__":
    benchmark()
