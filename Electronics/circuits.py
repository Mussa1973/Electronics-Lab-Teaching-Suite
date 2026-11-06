"""
Time-domain simulations for RC, RL, and RLC circuits.
Used for classroom demonstrations and student exercises.
"""

import numpy as np


class RCCircuit:
    """RC low-pass / high-pass circuit simulation."""

    def __init__(self, R: float, C: float, Vin: float = 1.0):
        self.R = R          # ohms
        self.C = C          # farads
        self.Vin = Vin      # volts
        self.tau = R * C    # time constant (s)

    def cutoff_frequency(self) -> float:
        """fc = 1 / (2πRC)"""
        return 1.0 / (2 * np.pi * self.R * self.C)

    def step_response(self, t_end: float = None, points: int = 500) -> tuple[np.ndarray, np.ndarray]:
        """Capacitor voltage response to a step input (charging)."""
        if t_end is None:
            t_end = 5 * self.tau
        t = np.linspace(0, t_end, points)
        Vc = self.Vin * (1 - np.exp(-t / self.tau))
        return t, Vc

    def discharge_response(self, t_end: float = None, points: int = 500) -> tuple[np.ndarray, np.ndarray]:
        """Capacitor voltage during discharge."""
        if t_end is None:
            t_end = 5 * self.tau
        t = np.linspace(0, t_end, points)
        Vc = self.Vin * np.exp(-t / self.tau)
        return t, Vc

    def summary(self) -> dict:
        return {
            "R": self.R,
            "C": self.C,
            "tau_s": self.tau,
            "fc_Hz": self.cutoff_frequency(),
            "V_steady": self.Vin,
        }


class RLCircuit:
    """Series RLC circuit — damping factor & resonant frequency."""

    def __init__(self, R: float, L: float, C: float):
        self.R, self.L, self.C = R, L, C

    def resonant_frequency(self) -> float:
        """f0 = 1 / (2π√(LC))"""
        return 1.0 / (2 * np.pi * np.sqrt(self.L * self.C))

    def damping_factor(self) -> float:
        """ζ = (R/2) * √(C/L)"""
        return (self.R / 2) * np.sqrt(self.C / self.L)

    def response_type(self) -> str:
        z = self.damping_factor()
        if z < 1:
            return "Underdamped (oscillatory)"
        elif np.isclose(z, 1):
            return "Critically damped"
        else:
            return "Overdamped"

    def step_response(self, t_end: float = None, points: int = 1000) -> tuple[np.ndarray, np.ndarray]:
        """Simulate step response numerically (state-space integration)."""
        if t_end is None:
            t_end = 10 / self.resonant_frequency()
        dt = t_end / points
        t = np.linspace(0, t_end, points)

        # State: [i_L, v_C]
        i, v = 0.0, 0.0
        out = np.zeros(points)
        for k in range(points):
            di = (1.0 - v - self.R * i) / self.L
            dv = i / self.C
            i += di * dt
            v += dv * dt
            out[k] = v
        return t, out