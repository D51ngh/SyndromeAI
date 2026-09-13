def logical_failure(logical_observable: int, decoder_prediction: int) -> int:
    return int(logical_observable != decoder_prediction)
