import argparse
from pathlib import Path

import numpy as np
import pandas as pd


def inspect(input_dir):
    root = Path(input_dir)
    detectors = np.load(root / "detectors.npz")["detectors"]
    metadata = pd.read_csv(root / "metadata.csv")
    metadata["detector_count"] = detectors.sum(axis=1)
    metadata["first_detector"] = [int(np.flatnonzero(row)[0]) if row.any() else -1 for row in detectors]
    metadata["last_detector"] = [int(np.flatnonzero(row)[-1]) if row.any() else -1 for row in detectors]
    print(metadata.groupby("fault_type")["detector_count"].agg(["mean", "std", "count"]).round(4))
    return metadata


if __name__ == "__main__":
    parser = argparse.ArgumentParser(); parser.add_argument("--input", default="data/raw/phase1"); args = parser.parse_args(); inspect(args.input)
