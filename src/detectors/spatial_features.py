import numpy as np


def active_detector_indices(history: np.ndarray) -> np.ndarray:
    return np.flatnonzero(np.asarray(history))
