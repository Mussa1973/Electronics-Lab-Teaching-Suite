"""
Unit tests for the electronics simulation package.
Run with: pytest tests/
"""

import math
import numpy as np
import pytest

from electronics.circuits import RCCircuit, RLCircuit
from electronics.filters import LowPassFilter, HighPassFilter
from electronics.opamp import InvertingAmplifier, NonInvertingAmplifier, VoltageFollower
from electronics.transistor import BJTVoltageDivider
from electronics.utils import format_si, db


# ---------- RC ----------
def test_rc_time_constant():
    rc = RCCircuit(R=1_000, C=10e-6)
    assert rc.tau == pytest.approx(0.01)


def test_rc_cutoff_frequency():
    rc = RCCircuit(R=1_000, C=10e-6)
    expected = 1 / (2 * math.pi * 1_000 * 10e-6)
    assert rc.cutoff_frequency() == pytest.approx(expected)


def test_rc_charging_at_tau():
    rc = RCCircuit(R=1_000, C=10e-6)
    t, v = rc.step_response()
    idx = np.argmin(np.abs(t - rc.tau))
    assert v[idx] == pytest.approx(0.632, abs=0.01)


def test_rc_discharge_at_tau():
    rc = RCCircuit(R=1_000, C=10e-6)
    t, v = rc.discharge_response()
    idx = np.argmin(np.abs(t - rc.tau))
    assert v[idx] == pytest.approx(0.368, abs=0.01)


# ---------- RLC ----------
def test_rlc_resonant_frequency():
    rlc = RLCircuit(R=200, L=10e-3, C=1e-6)
    assert rlc.resonant_frequency() == pytest.approx(1591.55, rel=1e-3)


def test_rlc_critical_damping():
    rlc = RLCircuit(R=200, L=10e-3, C=1e-6)
    assert rlc.damping_factor() == pytest.approx(1.0)
    assert "Critical" in rlc.response_type()


def test_rlc_underdamped():
    rlc = RLCircuit(R=50, L=10e-3, C=1e-6)
    assert rlc.damping_factor() < 1
    assert "Underdamped" in rlc.response_type()


# ---------- Filters ----------
def test_lpf_gain_at_cutoff():
    lpf = LowPassFilter(R=1_000, C=10e-6)
    fc = lpf.cutoff_frequency()
    _, H = lpf.frequency_response(freqs=np.array([fc]))
    mag_db = 20 * np.log10(abs(H[0]))
    assert mag_db == pytest.approx(-3.01, abs=0.05)


def test_hpf_attenuates_low_freq():
    hpf = HighPassFilter(R=1_000, C=10e-6)
    fc = hpf.cutoff_frequency()
    _, H = hpf.frequency_response(freqs=np.array([fc / 100]))
    assert abs(H[0]) < 0.02


# ---------- Op-Amp ----------
def test_inverting_gain():
    amp = InvertingAmplifier(R_in=1_000, R_f=10_000)
    assert amp.gain() == pytest.approx(-10)


def test_non_inverting_gain():
    amp = NonInvertingAmplifier(R1=1_000, R2=9_000)
    assert amp.gain() == pytest.approx(10)


def test_voltage_follower():
    assert VoltageFollower().gain() == 1.0


# ---------- BJT ----------
def test_bjt_q_point():
    q = BJTVoltageDivider(Vcc=12, R1=47_000, R2=10_000,
                          Rc=2_200, Re=1_000, beta=150)
    assert q.base_voltage() == pytest.approx(12 * 10_000 / 57_000, rel=1e-3)
    assert q.emitter_voltage() == pytest.approx(q.base_voltage() - 0.7)
    assert 0 < q.collector_voltage() < 12


# ---------- Utils ----------
def test_format_si():
    assert "k" in format_si(1_500, "Ω")
    assert "µ" in format_si(10e-6, "F")
    assert "m" in format_si(0.01, "s")


def test_db():
    assert db(1) == pytest.approx(0)
    assert db(10) == pytest.approx(20)
    assert db(100) == pytest.approx(40)