from dataclasses import dataclass


@dataclass(frozen=True)
class CircuitLocation:
    fault_type: str
    round_index: int
    site_index: int
    location: str
    qubits: str
