from src.noise.cnot_error import cnot_fault_gate
from src.noise.measurement_error import measurement_flip_gate


def test_fault_gate_names():
    assert measurement_flip_gate() == "X_ERROR"
    assert cnot_fault_gate() == "DEPOLARIZE2"
