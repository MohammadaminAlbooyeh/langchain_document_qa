#!/usr/bin/env python3
import shutil
from pathlib import Path


def main():
    dirs = [Path("./chroma_db"), Path("./data/processed/embeddings"), Path("./data/processed/splits")]
    for d in dirs:
        if d.exists():
            shutil.rmtree(d)
            print(f"Cleaned up {d}")
    print("Cleanup complete!")


if __name__ == "__main__":
    main()
