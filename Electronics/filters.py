"""
Frequency response of passive filters — for Bode plots in class.
"""

import numpy as np
from Electronics.circuits import RCCircuit

class LowPassFilter:
    """First-order RC low-pass filter."""

    def __init__(self, R: float, C: float):
        self.rc = RCCircuit(R, C)

    def frequency_response(self, freqs: np.ndarray = None) -> tuple[np.ndarray, np.ndarray]:
        if freqs is None:
            fc = self.rc.cutoff_frequency()
            freqs = np.logspace(np.log10(fc) - 2, np.log10(fc) + 2, 400)
        fc = self.rc.cutoff_frequency()
        H = 1 / (1 + 1j * freqs / fc)
        return freqs, H

    def cutoff_frequency(self) -> float:
        return self.rc.cutoff_frequency()

class HighPassFilter:
    """First-order RC high-pass filter."""

    def __init__(self, R: float, C: float):
        self.rc = RCCircuit(R, C)

    def frequency_response(self, freqs: np.ndarray = None) -> tuple[np.ndarray, np.ndarray]:
        if freqs is None:
            fc = self.rc.cutoff_frequency()
            freqs = np.logspace(np.log10(fc) - 2, np.log10(fc) + 2, 400)
        fc = self.rc.cutoff_frequency()
        H = (1j * freqs / fc) / (1 + 1j * freqs / fc)
        return freqs, H

    def cutoff_frequency(self) -> float:          # ✅ ADD THIS
        """fc = 1 / (2πRC) — same for high-pass and low-pass."""
        return self.rc.cutoff_frequency()

class BandPassFilter:
    """Series RLC band-pass filter."""

    def __init__(self, R: float, L: float, C: float):
        from .circuits import RLCircuit
        self.rlc = RLCircuit(R, L, C)

    def frequency_response(self, freqs: np.ndarray = None) -> tuple[np.ndarray, np.ndarray]:
        f0 = self.rlc.resonant_frequency()
        if freqs is None:
            freqs = np.logspace(np.log10(f0) - 2, np.log10(f0) + 2, 400)
        Q = 1 / (2 * self.rlc.damping_factor())
        H = 1 / (1 + 1j * Q * (freqs / f0 - f0 / freqs))
        return freqs, H