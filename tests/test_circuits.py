from src.circuits.build_surface_code import build_surface_code


def test_surface_code_builds():
    circuit=build_surface_code(3,3)
    assert circuit.num_qubits > 0
    assert circuit.num_detectors > 0
