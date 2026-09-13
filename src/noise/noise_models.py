from dataclasses import dataclass


@dataclass(frozen=True)
class FaultLabel:
    fault_type: str
    round_index: int = 0
    site_index: int = -1
    location: str = "none"
    qubits: str = "none"
