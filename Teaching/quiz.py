"""
Auto-generated quiz bank for second-year electronics.
"""

import random


QUESTIONS = [
    {
        "q": "What is the time constant τ of an RC circuit with R=2 kΩ and C=4.7 µF?",
        "options": ["9.4 ms", "4.7 ms", "2 ms", "0.94 ms"],
        "answer": 0,
        "explain": "τ = RC = 2000 × 4.7e-6 = 9.4 ms",
    },
    {
        "q": "The cutoff frequency of a first-order RC low-pass filter is:",
        "options": ["1/(RC)", "1/(2πRC)", "2πRC", "RC/2π"],
        "answer": 1,
        "explain": "fc = 1/(2πRC)",
    },
    {
        "q": "A series RLC circuit has R=100Ω, L=10mH, C=1µF. What is f0?",
        "options": ["1.59 kHz", "15.9 kHz", "159 Hz", "1.59 MHz"],
        "answer": 0,
        "explain": "f0 = 1/(2π√(LC)) = 1/(2π√(10e-3 × 1e-6)) ≈ 1.59 kHz",
    },
    {
        "q": "In a non-inverting op-amp with R1=1kΩ, R2=9kΩ, the gain is:",
        "options": ["-9", "10", "-10", "9"],
        "answer": 1,
        "explain": "Gain = 1 + R2/R1 = 1 + 9 = 10",
    },
    {
        "q": "A BJT has β=100, I_B=20µA. What is I_C?",
        "options": ["2 mA", "20 mA", "0.2 mA", "200 mA"],
        "answer": 0,
        "explain": "I_C = β × I_B = 100 × 20µA = 2 mA",
    },
    {
        "q": "Which damping factor gives critical damping?",
        "options": ["ζ = 0", "ζ = 0.5", "ζ = 1", "ζ > 1"],
        "answer": 2,
        "explain": "Critical damping occurs at ζ = 1",
    },
    {
        "q": "At what frequency does a first-order LPF attenuate by 3 dB?",
        "options": ["fc/2", "fc", "2fc", "10fc"],
        "answer": 1,
        "explain": "At fc, gain is -3 dB by definition",
    },
    {
        "q": "The voltage gain in dB of a ×100 amplifier is:",
        "options": ["20 dB", "40 dB", "60 dB", "100 dB"],
        "answer": 1,
        "explain": "20·log10(100) = 40 dB",
    },
]


def get_random_question() -> dict:
    """Return a shuffled question with shuffled options."""
    q = random.choice(QUESTIONS).copy()
    correct_text = q["options"][q["answer"]]
    random.shuffle(q["options"])
    q["answer"] = q["options"].index(correct_text)
    return q