import stim


def inject_measurement_error(circuit, measurement_index):
    """Flip one measured ancilla record before measurement.

    X_ERROR is used instead of deterministic X so Stim treats it as a fault
    relative to the ideal detector expectations.
    """
    result = stim.Circuit()
    index = 0
    for instruction in circuit.flattened():
        targets = instruction.targets_copy()
        if instruction.name == "MR":
            for target in targets:
                if index == measurement_index:
                    result.append("X_ERROR", [target.value], [1.0])
                index += 1
            result.append("M", targets)
            result.append("R", targets)
        else:
            result.append(instruction.name, targets, instruction.gate_args_copy())
    return result
