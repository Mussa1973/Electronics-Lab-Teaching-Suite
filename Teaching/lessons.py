"""
Structured lessons for second-year electronics students.
Each lesson = theory + live Python example + class exercise.
"""

from Electronics.circuits import RCCircuit, RLCircuit
from Electronics.filters import LowPassFilter, HighPassFilter
from Electronics.opamp import InvertingAmplifier, NonInvertingAmplifier
from Electronics.transistor import BJTVoltageDivider
from Electronics.utils import format_si


LESSONS = {
    "1. RC Circuit — Time Constant": {
        "theory": (
            "The RC circuit's time constant τ = RC defines how fast a capacitor "
            "charges/discharges. After 1τ it reaches 63.2% of final voltage; "
            "after 5τ it's effectively at steady state. The cutoff frequency "
            "fc = 1/(2πRC) is where the output drops by 3 dB."
        ),
        "demo": lambda: _demo_rc(),
        "exercise": "Design an RC circuit with τ = 10 ms using a 1 kΩ resistor. What C do you need?",
        "answer": "C = τ/R = 10e-3 / 1e3 = 10 µF",
    },
    "2. Low-Pass Filter — Bode Plot": {
        "theory": (
            "A first-order RC low-pass filter passes frequencies below fc and "
            "attenuates above it at -20 dB/decade. At fc the gain is -3 dB and "
            "phase is -45°."
        ),
        "demo": lambda: _demo_lpf(),
        "exercise": "What is the attenuation at 10× fc for a first-order LPF?",
        "answer": "-20 dB (one decade → -20 dB/decade)",
    },
    "3. RLC Resonance — Damping": {
        "theory": (
            "Series RLC circuits resonate at f0 = 1/(2π√(LC)). The damping factor "
            "ζ = (R/2)·√(C/L) determines response: underdamped (ζ<1), critically "
            "damped (ζ=1), or overdamped (ζ>1). Quality factor Q = 1/(2ζ)."
        ),
        "demo": lambda: _demo_rlc(),
        "exercise": "For L=10 mH, C=1 µF, what R gives critical damping?",
        "answer": "ζ=1 → R = 2√(L/C) = 2√(10e-3/1e-6) = 2×100 = 200 Ω",
    },
    "4. Op-Amp — Inverting & Non-Inverting": {
        "theory": (
            "Ideal op-amp has infinite gain, infinite input impedance, zero output "
            "impedance. Inverting gain = -Rf/Rin. Non-inverting gain = 1 + R2/R1. "
            "Feedback sets the closed-loop gain."
        ),
        "demo": lambda: _demo_opamp(),
        "exercise": "Design a non-inverting amp with gain 11 using R1=10 kΩ.",
        "answer": "Gain = 1 + R2/R1 = 11 → R2/R1 = 10 → R2 = 100 kΩ",
    },
    "5. BJT Voltage-Divider Bias": {
        "theory": (
            "Voltage-divider bias is the most stable BJT biasing method. "
            "V_B = Vcc·R2/(R1+R2), V_E = V_B - 0.7, I_E = V_E/Re, "
            "V_C = Vcc - I_C·Rc. The bias point (Q-point) must sit mid-load-line "
            "for maximum symmetric swing."
        ),
        "demo": lambda: _demo_bjt(),
        "exercise": "For Vcc=12V, R1=47k, R2=10k, Re=1k, Rc=2.2k, β=150 — find I_C and V_C.",
        "answer": "V_B≈2.1V, V_E=1.4V, I_E=1.4mA, I_C≈1.39mA, V_C≈12-1.39m×2.2k≈8.94V",
    },
}


def _demo_rc():
    rc = RCCircuit(R=1_000, C=10e-6)
    return rc.summary()


def _demo_lpf():
    lpf = LowPassFilter(R=1_000, C=10e-6)
    return {"fc": format_si(lpf.cutoff_frequency(), "Hz")}


def _demo_rlc():
    rlc = RLCircuit(R=200, L=10e-3, C=1e-6)
    return {
        "f0": format_si(rlc.resonant_frequency(), "Hz"),
        "ζ": f"{rlc.damping_factor():.3f}",
        "type": rlc.response_type(),
    }


def _demo_opamp():
    inv = InvertingAmplifier(R_in=1_000, R_f=10_000)
    non = NonInvertingAmplifier(R1=1_000, R2=10_000)
    return {"inverting_gain": inv.gain(), "non_inverting_gain": non.gain()}


def _demo_bjt():
    q = BJTVoltageDivider(Vcc=12, R1=47_000, R2=10_000, Rc=2_200, Re=1_000, beta=150)
    return q.summary()