def risk_amplification(pattern_failure_rate, baseline_failure_rate):
    if baseline_failure_rate == 0:
        return float("inf") if pattern_failure_rate > 0 else 1.0
    return pattern_failure_rate / baseline_failure_rate
