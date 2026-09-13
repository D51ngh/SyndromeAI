import numpy as np


def active_span(history: np.ndarray) -> tuple[int, int]:
    active = np.flatnonzero(np.asarray(history))
    return (-1, -1) if len(active) == 0 else (int(active[0]), int(active[-1]))
