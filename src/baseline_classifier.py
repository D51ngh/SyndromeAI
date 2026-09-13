import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split


def train(input_dir, seed=0):
    root = Path(input_dir)
    x = np.load(root / "detectors.npz")["detectors"]
    metadata = pd.read_csv(root / "metadata.csv")
    y = metadata["class_id"].to_numpy()
    train_x, test_x, train_y, test_y = train_test_split(x, y, test_size=0.25, random_state=seed, stratify=y)
    model = LogisticRegression(max_iter=1000, random_state=seed)
    model.fit(train_x, train_y)
    prediction = model.predict(test_x)
    print(classification_report(test_y, prediction, target_names=["none", "measurement", "cnot"], zero_division=0))
    print("confusion matrix (rows=true, columns=predicted):\n", confusion_matrix(test_y, prediction))
    return model


if __name__ == "__main__":
    parser = argparse.ArgumentParser(); parser.add_argument("--input", default="data/raw/phase1"); args = parser.parse_args(); train(args.input)
