import numpy as np
from src.detectors.detector_history import detector_count
from src.detectors.temporal_features import active_span


def test_detector_features():
    values=np.array([0,1,0,1])
    assert detector_count(values) == 2
    assert active_span(values) == (1,3)
