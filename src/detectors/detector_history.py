import numpy as np


def detector_count(history: np.ndarray) -> int:
    return int(np.asarray(history).sum())
