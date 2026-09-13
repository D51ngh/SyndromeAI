import argparse
import csv
from pathlib import Path

import numpy as np

try:
    from .build_surface_code import build_surface_code
    from .inject_measurement_error import inject_measurement_error
    from .inject_cnot_error import inject_cnot_error
except ImportError:  # Supports direct execution: python src/generate_dataset.py
    from build_surface_code import build_surface_code
    from inject_measurement_error import inject_measurement_error
    from inject_cnot_error import inject_cnot_error


def _site_counts(circuit):
    measurements = sum(len(i.targets_copy()) for i in circuit.flattened() if i.name == "MR")
    cnots = sum(len(i.targets_copy()) // 2 for i in circuit.flattened() if i.name == "CX")
    return measurements, cnots


def generate_dataset(output, samples_per_class=100, distance=3, rounds=3, seed=1234):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    base = build_surface_code(distance, rounds)
    measurement_count, cnot_count = _site_counts(base)
    rng = np.random.default_rng(seed)
    patterns, rows = [], []
    for fault_type, class_id in (("none", 0), ("measurement", 1), ("cnot", 2)):
        for sample_index in range(samples_per_class):
            if fault_type == "none":
                location, site_index, circuit = "none", -1, base
                qubits = "none"
            elif fault_type == "measurement":
                site_index = int(rng.integers(measurement_count))
                location, qubits = "measurement", str(site_index)
                circuit = inject_measurement_error(base, site_index)
            else:
                site_index = int(rng.integers(cnot_count))
                location, qubits = "CNOT", str(site_index)
                circuit = inject_cnot_error(base, site_index)
            detectors, observables = circuit.compile_detector_sampler(seed=int(rng.integers(2**31))).sample(1, separate_observables=True)
            patterns.append(detectors[0].astype(np.uint8))
            rows.append({"sample_id": len(rows), "fault_type": fault_type, "class_id": class_id, "site_index": site_index, "location": location, "qubits": qubits, "logical_outcome": int(observables[0, 0])})
    np.savez_compressed(output / "detectors.npz", detectors=np.stack(patterns), class_id=np.array([r["class_id"] for r in rows]))
    with (output / "metadata.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)
    return output / "detectors.npz", output / "metadata.csv"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(); parser.add_argument("--output", default="data/raw/phase1"); parser.add_argument("--samples-per-class", type=int, default=100); parser.add_argument("--distance", type=int, default=3); parser.add_argument("--rounds", type=int, default=3); parser.add_argument("--seed", type=int, default=1234); args = parser.parse_args(); print(generate_dataset(args.output, args.samples_per_class, args.distance, args.rounds, args.seed))
