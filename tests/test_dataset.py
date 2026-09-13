import numpy as np
import pandas as pd
from src.simulation.generate_samples import generate_dataset


def test_dataset_generation(tmp_path):
    arrays, metadata_path=generate_dataset(tmp_path, samples_per_class=2, distance=3, rounds=3, seed=1)
    assert np.load(arrays)["detectors"].shape == (6,24)
    assert set(pd.read_csv(metadata_path)["fault_type"]) == {"none","measurement","cnot"}
