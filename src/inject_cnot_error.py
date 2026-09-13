import stim


def inject_cnot_error(circuit, cnot_index):
    """Insert a known two-qubit depolarizing fault after one CNOT pair."""
    result = stim.Circuit()
    index = 0
    for instruction in circuit.flattened():
        targets = instruction.targets_copy()
        if instruction.name == "CX":
            result.append("CX", targets)
            for start in range(0, len(targets), 2):
                pair = targets[start:start + 2]
                if index == cnot_index:
                    result.append("DEPOLARIZE2", [pair[0].value, pair[1].value], [1.0])
                index += 1
        else:
            result.append(instruction.name, targets, instruction.gate_args_copy())
    return result
