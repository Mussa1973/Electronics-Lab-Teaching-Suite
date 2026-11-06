"""
Ideal op-amp configurations — worked examples for class.
"""


class OpAmpConfig:
    """Base class for ideal op-amp configurations."""

    def gain(self) -> float:
        raise NotImplementedError

    def summary(self) -> dict:
        raise NotImplementedError


class InvertingAmplifier(OpAmpConfig):
    def __init__(self, R_in: float, R_f: float):
        self.R_in, self.R_f = R_in, R_f

    def gain(self) -> float:
        return -self.R_f / self.R_in

    def summary(self) -> dict:
        return {"Type": "Inverting", "Gain": self.gain(),
                "R_in": self.R_in, "R_f": self.R_f}


class NonInvertingAmplifier(OpAmpConfig):
    def __init__(self, R1: float, R2: float):
        self.R1, self.R2 = R1, R2

    def gain(self) -> float:
        return 1 + self.R2 / self.R1

    def summary(self) -> dict:
        return {"Type": "Non-inverting", "Gain": self.gain(),
                "R1": self.R1, "R2": self.R2}


class VoltageFollower(OpAmpConfig):
    def gain(self) -> float:
        return 1.0

    def summary(self) -> dict:
        return {"Type": "Voltage follower (buffer)", "Gain": 1.0}