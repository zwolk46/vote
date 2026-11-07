"""Tests for pipeline/college.py and the checks pipeline/president.py relies on.

Written 2026-11-07 by worker D1. Run:  python3 pipeline/test_college.py   (or pytest pipeline/)
Each test says what it guards and why.
"""
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import college  # noqa: E402

ROOT = os.path.dirname(HERE)


def test_window_weights():
    """The flip decides outright between 270 - e and 268, and by half at the two 269 endpoints (S4's rule)."""
    w = college.window_weights(20, 538, 270)
    assert w[248] == 0 and w[249] == 0.5 and w[250] == 1 and w[268] == 1 and w[269] == 0.5 and w[270] == 0
    # an odd total (1960: 537, majority 269) has no College tie, so no half weights
    w = college.window_weights(10, 537, 269)
    assert set(np.unique(w)) <= {0.0, 1.0} and w[259] == 1 and w[268] == 1 and w[258] == 0


def test_swing_model_equals_closed_form():
    """With normal errors the grid posterior must equal S4's closed-form conditional (dp_stage_two), so the
    t4 version is the same computation with another density."""
    rng = np.random.default_rng(0)
    mu = 0.5 + rng.normal(0, 0.08, 51)
    ev = np.full(51, 10)
    ev[:28] += 1                      # 538 votes in all
    assert ev.sum() == 538
    tau, s_d = np.full(51, 0.04), 0.025
    for i in (0, 7, 20):
        closed = college.dp_stage_two(i, mu, tau, ev, s_d, 538, 270)
        grid = college.swing_model(i, mu, np.sqrt(tau ** 2 - s_d ** 2), ev, s_d, 538, 270, "normal")
        assert abs(grid["W"] - closed[0]) <= 1e-6 * max(closed[0], 1e-12) + 1e-12, (i, grid["W"], closed[0])
        assert abs(grid["W_unconditional"] - closed[1]) <= 1e-6 * closed[1] + 1e-12
        f = math.exp(-0.5 * ((0.5 - mu[i]) / 0.04) ** 2) / (0.04 * math.sqrt(2 * math.pi))
        assert abs(grid["f_half"] - f) < 1e-6 * f


def test_t4_cdf():
    """The t4 cdf's closed form: symmetric, 1/2 at 0, and its known 97.5% point 2.776."""
    assert abs(college._t4_cdf(0.0) - 0.5) < 1e-15
    assert abs(college._t4_cdf(2.7764451) - 0.975) < 1e-6
    assert abs(college._t4_cdf(-1.3) + college._t4_cdf(1.3) - 1) < 1e-15


def test_sims_window_toy():
    """Three units of 3, 3 and 1 votes (total 7, majority 4): unit 0 decides when the other two give A
    1 to 3 votes; counted on hand-made draws, one with unit 0 printed at exactly one half."""
    shares = np.array([[0.5000, 0.6, 0.4],     # unit 0 at one half (ambiguous), unit 1 for A: E_rest = 3
                       [0.5003, 0.4, 0.6],     # unit 0 for A, unit 2 for A: E_rest = 1
                       [0.4990, 0.6, 0.6],     # E_rest = 4: A already wins, unit 0 does not decide
                       [0.6000, 0.4, 0.4]])    # outside the window
    ev = [3, 3, 1]
    dem_ev = np.array([6, 4, 4, 3])            # draw 0: the ambiguous unit went to A (3 + 3)
    c = college.sims_window(shares, dem_ev, ev, 0, 10, 1e-4, 7, 4)
    assert c["in_window"] == 3 and c["dropped_unclear"] == 0
    # weights: E_rest 3 -> win(6) - win(3) = 1; E_rest 1 -> win(4) - win(1) = 1; E_rest 4 -> 0
    assert c["weighted"] == 2.0 and c["decisive_full"] == 2 and c["draws_total_mismatch"] == 0


def test_poisson_upper():
    """Zero events seen: the 95% upper bound on the mean is -ln(0.05) = 2.996."""
    import president
    assert abs(president.poisson_upper(0) - 2.995732) < 1e-4
    assert 6.29 < president.poisson_upper(2) < 6.31


def test_economist_pa_reproduction():
    """The check in REPORT.md: from the Economist's draws, Pennsylvania 2020 comes out within 2% of its own
    p_decisive_vote. Guards the draws' intake and the window arithmetic."""
    path = os.path.join(ROOT, "data", "president", "2020.json")
    if not os.path.exists(path):
        return
    d = json.load(open(path))
    pa = next(c for c in d["contests"] if c["id"] == "2020-president-PA")
    e = next(f for f in pa["forecasts"] if f["by"] == "The Economist")
    assert 0.98 < e["p"]["ratio_to_published"] < 1.02, e["p"]["ratio_to_published"]


def test_sd_rel_error():
    """The orchestrator's rule of 04:20: 538's implied sd is kept where its estimated relative error is under
    20%. A chance of exactly 0 or 1 always falls back; a chance of one run in 20,000 falls back (about 50%,
    since one standard error below it is nearly 0); Florida 2016
    (538's 53.675%, mean 0.5027) comes out near 10% and keeps 538."""
    import president
    r = {"win_prob": 1.0, "mean": 0.9, "probwin_other": 0.0, "share_D": 90.0, "share_R": 10.0,
         "half_step_D": 5e-6, "half_step_R": 5e-6}
    assert president.implied_sd_breaks(r, 20000, 5e-5)[0] is not None
    r.update(win_prob=0.00005, mean=0.40)
    why, err = president.implied_sd_breaks(r, 20000, 5e-5)
    assert why is not None and err["value"] > 0.2
    path = os.path.join(ROOT, "data", "president", "2016.json")
    if os.path.exists(path):
        d = json.load(open(path))
        fl = next(c for c in d["contests"] if c["id"] == "2016-president-FL")
        f = next(f for f in fl["forecasts"] if f["by"] == "538" and f["model"] == "polls-plus")
        assert 0.09 < f["share"]["sd_rel_error"]["value"] < 0.10 and f["p"] is not None
        # the amendment of 05:58 (M2 3.9): the rule is on p's error, |z^2 - 1| times the sd's. California 2016
        # (z = 3.48) has a small sd error but a p error of about 50%, so the model's own stands first there
        ca = next(c for c in d["contests"] if c["id"] == "2016-president-CA")
        f = next(f for f in ca["forecasts"] if f["by"] == "538" and f["model"] == "polls-plus")
        assert f["share"]["sd_rel_error"]["value"] < 0.05 and f["share"]["p_rel_error"]["value"] > 0.2
        assert f["p"] is None and ca["p"]["under"] == "the model's own"


def test_economist_thin_window():
    """The amendment of 05:58 (M2 2.4): the Economist's W is marked thin under 30 weighted draws (OH, IA, CO)."""
    path = os.path.join(ROOT, "data", "president", "2020.json")
    if not os.path.exists(path):
        return
    d = json.load(open(path))
    thin = sorted(c["place"]["state"] for c in d["contests"] if (c["p"] or {}).get("W_thin"))
    assert thin == ["CO", "IA", "OH"], thin


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print(f"ok  {name}")
