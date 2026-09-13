import stim


def build_surface_code(distance: int = 3, rounds: int = 3) -> stim.Circuit:
    if distance < 3 or distance % 2 == 0:
        raise ValueError("distance must be an odd integer >= 3")
    if rounds < 1:
        raise ValueError("rounds must be positive")
    return stim.Circuit.generated("surface_code:rotated_memory_z", distance=distance, rounds=rounds)
