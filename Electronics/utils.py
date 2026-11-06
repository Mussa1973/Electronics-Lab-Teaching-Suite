"""Shared helpers for electronics calculations."""

import numpy as np


def format_si(value: float, unit: str) -> str:
    """Format a value with SI prefix (k, M, m, µ, n, p)."""
    if value == 0:
        return f"0 {unit}"
    prefixes = [
        (1e9, "G"), (1e6, "M"), (1e3, "k"),
        (1, ""), (1e-3, "m"), (1e-6, "µ"),
        (1e-9, "n"), (1e-12, "p"),
    ]
    abs_v = abs(value)
    for factor, prefix in prefixes:
        if abs_v >= factor:
            return f"{value / factor:.3g} {prefix}{unit}"
    return f"{value:.3g} {unit}"


def db(gain: float) -> float:
    """Convert linear gain to decibels."""
    if gain <= 0:
        return -np.inf
    return 20 * np.log10(gain)