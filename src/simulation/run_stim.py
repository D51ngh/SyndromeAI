import numpy as np
import stim


def sample_detectors(circuit: stim.Circuit, seed: int) -> tuple[np.ndarray, int]:
    sampler = circuit.compile_detector_sampler(seed=seed)
    detectors, observables = sampler.sample(shots=1, separate_observables=True)
    return detectors[0].astype(np.uint8), int(observables[0, 0])
