"""
BJT biasing calculations — voltage divider bias.
"""


class BJTVoltageDivider:
    """NPN BJT with voltage-divider bias."""

    def __init__(self, Vcc: float, R1: float, R2: float,
                 Rc: float, Re: float, beta: float = 100):
        self.Vcc, self.R1, self.R2 = Vcc, R1, R2
        self.Rc, self.Re = Rc, Re
        self.beta = beta

    def base_voltage(self) -> float:
        return self.Vcc * self.R2 / (self.R1 + self.R2)

    def emitter_voltage(self) -> float:
        return self.base_voltage() - 0.7

    def emitter_current(self) -> float:
        return self.emitter_voltage() / self.Re

    def collector_current(self) -> float:
        return self.emitter_current() * self.beta / (self.beta + 1)

    def collector_voltage(self) -> float:
        return self.Vcc - self.collector_current() * self.Rc

    def summary(self) -> dict:
        return {
            "V_B (V)": self.base_voltage(),
            "V_E (V)": self.emitter_voltage(),
            "V_C (V)": self.collector_voltage(),
            "I_E (mA)": self.emitter_current() * 1000,
            "I_C (mA)": self.collector_current() * 1000,
        }