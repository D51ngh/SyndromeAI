import pymatching


def build_decoder(circuit):
    return pymatching.Matching.from_detector_error_model(circuit.detector_error_model())
