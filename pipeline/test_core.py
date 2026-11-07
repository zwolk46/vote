"""Tests for pipeline/core.py: it must reproduce the figures the model was checked with.

Run either way, from the repository root:
    python3 -m pytest pipeline
    python3 pipeline/test_core.py

Every expected figure below is copied from model/math/OUTPUT.txt (written by model/math/run_all.sh) or
from model/MATH.md, under the label given beside it, and is compared as OUTPUT.txt prints it: four
significant figures (common.fmt) and "1 in N" rounded to a whole number (common.one_in).
*Reason:* D2 and later workers compute every p through p_contest, so its figures must be the ones the
model was checked with (briefs/D1-data-president.md, step 1).
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import core  # noqa: E402
from core import p_contest, common  # noqa: E402

fmt = common.fmt


def test_town_race_of_2000():
    # OUTPUT.txt S6.5: "n = 2,000, mu = 0.52, tau = 0.04: exact p = 0.002137 (1 in 468)";
    # model section 2 and MATH section 6.2: "1 in 468". n sd^2 = 3.2 < 6.25, so "auto" takes the exact sum.
    r = p_contest(2000, 0.52, 0.04)
    assert r["method"] == "exact"
    assert fmt(r["p"]) == "0.002137"
    assert common.one_in(r["p"]) == "1 in 468"
    assert r["event"] == 2 * r["p"]


def test_sizes_in_the_m1_brief_exact():
    # OUTPUT.txt S6.5, the exact p of each row
    rows = [((300, 0.5, 0.05), "0.01149", "1 in 87"),
            ((2000, 0.52, 0.04), "0.002137", "1 in 468"),
            ((30000, 0.51, 0.03), "0.0002088", "1 in 4,789"),
            ((300000, 0.53, 0.025), "1.295e-05", "1 in 77,223"),
            ((3000000, 0.49, 0.02), "2.934e-06", "1 in 340,873"),
            ((9122861, 0.496, 0.0206), "1.042e-06", "1 in 960,105")]
    for (n, mu, sd), printed, one_in in rows:
        r = p_contest(n, mu, sd, method="exact")
        assert fmt(r["p"]) == printed, (n, mu, sd, r["p"])
        assert common.one_in(r["p"]) == one_in, (n, mu, sd, common.one_in(r["p"]))


def test_auto_is_within_the_models_stated_accuracy():
    # model section 3: "For races of 10,000 voters or more with a forecast spread of 2 points or more,
    # it is within 4%"; OUTPUT.txt S6.5 rows again, now through "auto"
    for n, mu, sd in [(30000, 0.51, 0.03), (300000, 0.53, 0.025), (3000000, 0.49, 0.02), (9122861, 0.496, 0.0206)]:
        a = p_contest(n, mu, sd)
        e = p_contest(n, mu, sd, method="exact")
        assert a["method"] == "density"
        assert abs(a["p"] / e["p"] - 1) < 0.01, (n, mu, sd, a["p"] / e["p"])


def test_density_form_s1_2():
    # OUTPUT.txt S1.2: f_v(1/2) and p = f/(2n), and the exact p beside it
    r = p_contest(10000, 0.5, 0.03, method="density")
    assert f"{r['f_half']:.4f}" == "13.2981" and fmt(r["p"]) == "0.0006649" and fmt(r["event"]) == "0.00133"
    assert fmt(p_contest(10000, 0.5, 0.03, method="exact")["p"]) == "0.0006558"
    r = p_contest(10000, 0.52, 0.03, method="density")
    assert f"{r['f_half']:.4f}" == "10.6483" and fmt(r["p"]) == "0.0005324"
    assert fmt(p_contest(10000, 0.52, 0.03, method="exact")["p"]) == "0.0005283"
    r = p_contest(92_000_000, 0.515, 0.056)
    assert r["method"] == "density" and f"{r['f_half']:.4f}" == "6.8729" and fmt(r["p"]) == "3.735e-08"
    # MATH section 2 table: GKB 1992 "ours 1 in 26,771,675" (S2.6)
    assert common.one_in(r["p"]) == "1 in 26,771,675"


def test_exact_below_the_thresholds_s1_3():
    # OUTPUT.txt S1.3, the exact p column; each of these is below 1,000 voters or below n sd^2 = 6.25
    rows = [((100, 0.5, 0.1), "0.01771"), ((300, 0.55, 0.03), "0.007736"), ((1000, 0.55, 0.03), "0.001981"),
            ((3000, 0.55, 0.03), "0.0005945"), ((3000, 0.5, 0.03), "0.00212"), ((1000, 0.5, 0.03), "0.005878")]
    for (n, mu, sd), printed in rows:
        r = p_contest(n, mu, sd)
        assert r["method"] == "exact", (n, mu, sd)
        assert fmt(r["p"]) == printed, (n, mu, sd, r["p"])


def test_t4_tails_s1_5():
    # OUTPUT.txt S1.5, n = 1,000,000, sd 0.03: "normal(sd 0.03)" and "t4(sd 0.03)" (the t4 matched on the
    # same sd, model section 9.5); both by the exact sum
    rows = {0.50: ("6.648e-06", "8.836e-06"), 0.52: ("5.324e-06", "5.353e-06"), 0.55: ("1.658e-06", "1.003e-06"),
            0.60: ("2.574e-08", "8.035e-08"), 0.70: ("1.494e-15", "3.402e-09")}
    for mu, (normal, t4) in rows.items():
        assert fmt(p_contest(1_000_000, mu, 0.03, "normal", "exact")["p"]) == normal, mu
        assert fmt(p_contest(1_000_000, mu, 0.03, "t4", "exact")["p"]) == t4, mu
        # and the density form of the t4 is within 0.1% of its exact sum at this size
        d = p_contest(1_000_000, mu, 0.03, "t4", "density")["p"]
        e = p_contest(1_000_000, mu, 0.03, "t4", "exact")["p"]
        assert abs(d / e - 1) < 1e-3, (mu, d / e)


def test_event_is_twice_p_and_side_symmetry():
    for args in [(2000, 0.52, 0.04), (1001, 0.48, 0.05), (5_000_000, 0.47, 0.02, "t4")]:
        r = p_contest(*args)
        assert r["event"] == 2 * r["p"]
    # at an even n the exact sum is the same for a ballot for either side
    a = p_contest(2000, 0.52, 0.04)["p"]
    b = p_contest(2000, 0.48, 0.04)["p"]
    assert abs(a / b - 1) < 1e-9
    # at an odd n the two sides differ by about |mean - 1/2| / (n sd^2) = 0.02 / (1001 x 0.0016) = 1.2%
    a = p_contest(1001, 0.52, 0.04)["p"]
    b = p_contest(1001, 0.48, 0.04)["p"]
    assert 0.005 < abs(a / b - 1) < 0.02
    # and once "auto" takes the density form, not at all
    assert p_contest(10001, 0.52, 0.04)["p"] == p_contest(10001, 0.48, 0.04)["p"]


def test_far_tail_never_returns_zero():
    # a very lopsided forecast: p is tiny but positive, as the site's "1 in N" needs
    r = p_contest(300_000, 0.93, 0.02)
    assert r["p"] > 0 and math.isfinite(r["p"])
    r = p_contest(500, 0.97, 0.005)
    assert r["p"] > 0 and math.isfinite(r["p"])


def test_bad_inputs_are_refused():
    for bad in [(0, 0.5, 0.03), (1000.0, 0.5, 0.03), (1000, 1.0, 0.03), (1000, 0.5, 0.0), (1000, 0.5, 0.03, "cauchy")]:
        try:
            p_contest(*bad)
        except ValueError:
            continue
        raise AssertionError(f"accepted {bad}")


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for t in tests:
        t()
        print(f"ok  {t.__name__}")
    print(f"{len(tests)} tests passed")
