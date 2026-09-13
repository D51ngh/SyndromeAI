import numpy as np


def predictive_entropy(probabilities):
    p=np.asarray(probabilities, dtype=float); p=np.clip(p, 1e-12, 1.0)
    return float(-(p*np.log(p)).sum())
