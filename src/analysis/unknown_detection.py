import numpy as np


def low_confidence(probabilities, threshold=0.6):
    p=np.asarray(probabilities); return bool(np.max(p) < threshold)
