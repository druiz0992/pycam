def clamp(current: float, delta: float, min_val: float, max_val: float) -> float:
    """
    Clamp  a delta so that (current + delta) stays within [min_val, max_val].

    Args:
        current: The current value.
        delta: The desired change.
        min_val: Minimum allowed value.
        max_val: Maximum allowed value.

    Returns:
        The adjusted delta that keeps the target within bounds.
    """
    target = max(min_val, min(current + delta, max_val))
    clamped = target - current
    return clamped
