"""Generate Phase-I detector histories with known fault labels."""

import argparse
import csv
from dataclasses import asdict
from pathlib import Path

import numpy as np
import stim

from src.circuits.build_surface_code import build_surface_code
from src.circuits.circuit_metadata import CircuitLocation
from src.simulation.run_stim import sample_detectors


def _sites(distance, rounds):
    circuit = build_surface_code(distance, rounds).flattened()
    measurements, cnots = [], []
    round_index, measurement_index, cnot_index = 1, 0, 0
    for instruction in circuit:
        targets = instruction.targets_copy()
        if instruction.name == "MR":
            for target in targets:
                measurements.append(CircuitLocation("measurement", round_index, measurement_index, f"round_{round_index}:measurement", str(target.value)))
                measurement_index += 1
            round_index += 1
        elif instruction.name == "CX":
            for i in range(0, len(targets), 2):
                a, b = targets[i:i + 2]
                cnots.append(CircuitLocation("cnot", round_index, cnot_index, f"round_{round_index}:CNOT", f"{a.value}-{b.value}"))
                cnot_index += 1
    return measurements, cnots


def inject_fault(distance, rounds, site):
    base = build_surface_code(distance, rounds).flattened()
    result = stim.Circuit()
    measurement_index = cnot_index = 0
    for instruction in base:
        targets = instruction.targets_copy()
        if instruction.name == "MR":
            for target in targets:
                if site.fault_type == "measurement" and measurement_index == site.site_index:
                    result.append("X_ERROR", [target.value], [1.0])
                measurement_index += 1
            result.append("M", targets)
            result.append("R", targets)
        elif instruction.name == "CX":
            result.append("CX", targets)
            for i in range(0, len(targets), 2):
                pair = targets[i:i + 2]
                if site.fault_type == "cnot" and cnot_index == site.site_index:
                    result.append("DEPOLARIZE2", [pair[0].value, pair[1].value], [1.0])
                cnot_index += 1
        else:
            result.append(instruction.name, targets, instruction.gate_args_copy())
    return result


def generate_dataset(output, samples_per_class=100, distance=3, rounds=3, seed=1234):
    output = Path(output); output.mkdir(parents=True, exist_ok=True)
    measurement_sites, cnot_sites = _sites(distance, rounds)
    rng = np.random.default_rng(seed); patterns=[]; rows=[]
    for fault_type, class_id in (("none", 0), ("measurement", 1), ("cnot", 2)):
        for sample_index in range(samples_per_class):
            if fault_type == "none":
                site = CircuitLocation("none", 0, -1, "none", "none"); circuit = build_surface_code(distance, rounds)
            else:
                site = (measurement_sites if fault_type == "measurement" else cnot_sites)[int(rng.integers(len(measurement_sites if fault_type == "measurement" else cnot_sites)))]
                circuit = inject_fault(distance, rounds, site)
            detector, logical = sample_detectors(circuit, int(rng.integers(2**31)))
            patterns.append(detector); row=asdict(site); row.update(sample_index=sample_index, class_id=class_id, logical_outcome=logical); rows.append(row)
    np.savez_compressed(output / "detectors.npz", detectors=np.stack(patterns), class_id=np.array([r["class_id"] for r in rows]))
    with (output / "metadata.csv").open("w", newline="") as handle:
        writer=csv.DictWriter(handle, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
    return output / "detectors.npz", output / "metadata.csv"


if __name__ == "__main__":
    parser=argparse.ArgumentParser(); parser.add_argument("--output", default="data/raw/phase1"); parser.add_argument("--samples-per-class", type=int, default=100); parser.add_argument("--distance", type=int, default=3); parser.add_argument("--rounds", type=int, default=3); parser.add_argument("--seed", type=int, default=1234); args=parser.parse_args(); print(generate_dataset(args.output, args.samples_per_class, args.distance, args.rounds, args.seed))
