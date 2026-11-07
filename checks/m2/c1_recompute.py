"""c1_recompute.py: recompute every p in data/ from its contest's own recorded inputs (brief M2, item 1).

For each contest with a p: the forecast p.under names is found among the contest's forecasts; from its
(n, mean, sd, tails) p is recomputed by M2's own code (m2lib, no pipeline import) and compared with the
record. Also checked: the event is exactly twice p; the exact lattice sum against the density form at
the sizes in the data; that every contest without p gives a reason; that every p names its forecast,
script and commit; and, for 538, that the implied sd is (mean - 1/2) / Phi^-1(chance).

Tolerances, and why. The density form p = f(1/2) / (2n) is closed-form arithmetic on the recorded inputs,
so the record and this recomputation must agree to floating-point precision: the tolerance is 1e-9
relative, and anything beyond it is an error in one of the two. The model's own presidential forecast
has f(1/2) as a numerical convolution (a normal national error and a t4 state error); D1 integrated it on
a 401-point grid, this check by adaptive quadrature, so 1e-4 relative is the tolerance there. 538's implied
sd in the Congress files is rounded to six decimals, so it is compared within its own rounding bound (the
mean's rounding, up to 5e-7, is a 3e-4 share of a mean 0.0015 from even, as in 2018-governor-NV). In the Congress files the forecast's
mean and sd are themselves recorded rounded to six decimals while p was computed from the unrounded
values, so a recomputation from the file can differ by up to (|z| + |z^2 - 1|) x 5e-7 / sd relative (z the
mean's distance from even in sds; for a mean 0.94 and sd 0.05 that is 7e-4). The tolerance there is this
bound, computed for each contest as the largest change of f(1/2) over the four corners of the rounding box
(mean +- 5e-7, sd +- 5e-7), plus 1e-9; the largest difference seen is printed, and so is the largest
difference as a share of its bound.
"""
import os
import re
import sys

import numpy as np
from scipy import stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m2lib as L  # noqa: E402

TOL_DENSITY = 1e-9      # the presidency: inputs recorded in full
ROUND = 5e-7            # Congress: the record's mean and sd are rounded to six decimals, p is not (see below)
TOL_CONV = 1e-4


def rel(a, b):
    if a is None or b is None:
        return None
    if b == 0:
        return abs(a)
    return abs(a / b - 1.0)


class Tally:
    def __init__(self):
        self.n = 0
        self.max = 0.0
        self.worst = None
        self.bad = []

    def add(self, name, got, rec, tol):
        self.n += 1
        r = rel(got, rec)
        if r is None:
            self.bad.append((name, got, rec, "missing"))
            return
        if r > self.max:
            self.max, self.worst = r, name
        if r > tol:
            self.bad.append((name, got, rec, r))


def report(title, t):
    print(f"  {title}: {t.n} compared, largest relative difference {t.max:.2e} ({t.worst}); "
          f"{len(t.bad)} beyond tolerance")
    for b in t.bad[:40]:
        print(f"     MISMATCH {b[0]}: recomputed {b[1]!r}, recorded {b[2]!r}, rel {b[3]}")


# ----------------------------------------------------------------------------------------- president
def check_president():
    print("1.1 The presidency: p_state = f(1/2) / (2 n) from the forecast p.under names, every contest")
    t_own, t_538, t_econ, t_event, t_prod = Tally(), Tally(), Tally(), Tally(), Tally()
    t_sd = Tally()
    n_p, n_nop, nop_without_reason, p_unnamed = 0, 0, [], []
    method_rule = []
    for path in L.president_files():
        d = L.load_json(path)
        for c in d["contests"]:
            p = c["p"]
            if not p:
                n_nop += 1
                if not any(s.startswith("No p") or s.startswith("No district count") for s in c.get("notes", [])):
                    nop_without_reason.append(c["id"])
                continue
            n_p += 1
            if not (p.get("under") and p.get("computed_by") and p.get("commit")):
                p_unnamed.append(c["id"])
            n = p["n_other_voters"]
            if n != c["result"]["two_party"] - 1:
                print(f"     n differs from two_party - 1: {c['id']}")
            t_event.add(c["id"], 2 * p["value"], p["event"], 0.0)
            t_prod.add(c["id"], p["p_state"] * p["W"], p["value"], 1e-12)
            # every forecast that carries its own p, not only the one shown first
            for f in c["forecasts"]:
                fp = f.get("p")
                if not fp:
                    continue
                tag = f"{c['id']} [{f['by']}{' ' + f['model'] if f.get('model') else ''}]"
                t_event.add(tag, 2 * fp["value"], fp["event"], 0.0)
                t_prod.add(tag, fp["p_state"] * fp["W"], fp["value"], 1e-12)
                sh = f["share"]
                if f["by"] == "the model's own":
                    fh = L.own_pres_pdf(0.5, sh["mean"], sh["national_sd"], sh["state_sd"])
                    t_own.add(tag, L.p_density(n, fh), fp["p_state"], TOL_CONV)
                    if abs(np.hypot(sh["national_sd"], sh["state_sd"]) / sh["sd"] - 1) > 1e-9:
                        print(f"     sd is not the root sum of squares: {tag}")
                elif f["by"] == "538":
                    fh = L.f_half(sh["mean"], sh["sd"], "normal")
                    t_538.add(tag, L.p_density(n, fh), fp["p_state"], TOL_DENSITY)
                    z = stats.norm.ppf(f["win_prob"])
                    t_sd.add(tag, (sh["mean"] - 0.5) / z, sh["sd"], 1e-9)
                    if n * sh["sd"] ** 2 < 6.25 or n < 1000:
                        method_rule.append(tag)
                elif f["by"] == "The Economist":
                    ps = fp["window_draws"] / (80000 * fp["window_width"]) / (2 * n)
                    t_econ.add(tag, ps, fp["p_state"], TOL_DENSITY)
                    W = fp["window_weighted"] / fp["window_draws"]
                    t_econ.add(tag + " W", W, fp["W"], TOL_DENSITY)
    print(f"  contests: {n_p} with p, {n_nop} without; without p and without a 'No p' note: "
          f"{nop_without_reason or 'none'}; p lacking under/computed_by/commit: {p_unnamed or 'none'}")
    report("the model's own: f(1/2) by quadrature vs the record (tolerance 1e-4)", t_own)
    report("538: normal density at the implied sd (tolerance 1e-9)", t_538)
    report("538: implied sd = (mean - 1/2) / Phi^-1(chance) (tolerance 1e-9)", t_sd)
    report("The Economist: window count / (K width) / (2n), and W = weighted / in-window", t_econ)
    report("event = 2 p (exact)", t_event)
    report("p = p_state x W (exact)", t_prod)
    print(f"  units where the model's rule would send p_state to the exact sum (n < 1,000 or n sd^2 < 6.25): "
          f"{method_rule or 'none'}")


# ------------------------------------------------------------------------------------------ congress
UNDER_538 = re.compile(r"^538 \((?P<v>[\w-]+)\)")
UNDER_OWN = re.compile(r"^the model's own \(D2-v1\), (?P<t>normal|t4)")


def forecast_for(c, under):
    m = UNDER_538.match(under)
    if m:
        v = m.group("v")
        for f in c["forecasts"]:
            if f["by"] == "538" and f.get("version") == v and f.get("share") and f["share"].get("sd"):
                return f, "normal"
        return None, None
    m = UNDER_OWN.match(under)
    if m:
        t = m.group("t")
        for f in c["forecasts"]:
            if f["by"] == "the model's own" and f["share"]["tails"] == t:
                return f, t
    return None, None


def check_congress(level):
    print(f"1.2 {level}: p = f(1/2) / (2 n) from the forecast p.under names, every contest, and every "
          "'alongside' p")
    t_p, t_event, t_fh, t_sd, t_ctl = Tally(), Tally(), Tally(), Tally(), Tally()
    n_p, n_zero, n_nop, nop_without_reason, zero_without_reason, unnamed, zero_unnamed = 0, 0, 0, [], [], [], []
    method_wrong, exact_rows, unmatched, share_of_bound = [], [], [], []
    rng = np.random.default_rng(7)
    for path in L.congress_files(level):
        d = L.load_json(path)
        for c in d["contests"]:
            p = c["p"]
            if p["value"] is None:
                n_nop += 1
                if not p.get("not_computed"):
                    nop_without_reason.append(c["id"])
                continue
            if p["value"] == 0:
                n_zero += 1
                if not p.get("reason"):
                    zero_without_reason.append(c["id"])
                if not (p.get("computed_by") and p.get("commit")):
                    zero_unnamed.append(c["id"])
                continue
            n_p += 1
            if not (p.get("under") and p.get("computed_by") and p.get("commit")):
                unnamed.append(c["id"])
            n = p["n"]
            if n != c["two_party"]["n_other_voters"] or n != sum(c["two_party"]["votes"]) - 1:
                print(f"     n differs from the two leading candidates' votes less one: {c['id']}")
            t_event.add(c["id"], 2 * p["value"], p["event"], 0.0)
            heads = [(p["under"], p)] + [(a["under"], a) for a in p.get("alongside", [])]
            for under, blk in heads:
                f, tails = forecast_for(c, under)
                tag = f"{c['id']} [{under[:28]}]"
                if f is None:
                    unmatched.append(tag)
                    continue
                mean, sd = f["share"]["mean"], f["share"]["sd"]
                fh = L.f_half(mean, sd, tails)
                tol = max(abs(L.f_half(mean + a, sd + b, tails) / fh - 1.0)
                          for a in (-ROUND, ROUND) for b in (-ROUND, ROUND)) + TOL_DENSITY
                t_fh.add(tag, fh, blk["f_half"], tol)
                t_p.add(tag, L.p_density(n, fh), blk["value"], tol)
                share_of_bound.append((rel(fh, blk["f_half"]) / tol, tag))
                t_event.add(tag, 2 * blk["value"], blk["event"], 0.0)
                rule = "exact" if (n < 1000 or n * sd * sd < 6.25) else "density"
                if blk["method"] != rule:
                    method_wrong.append((tag, blk["method"], rule, n, n * sd * sd))
                if f["by"] == "538":
                    ch = f["chance"]
                    dk = "D" if "D" in ch else "I"      # Sanders, King: the caucusing independent is the Democrat
                    q = ch[dk] / (ch[dk] + ch["R"])
                    isd = (mean - 0.5) / stats.norm.ppf(q)
                    # the bound of the recorded rounding: mean to six decimals, each chance to five
                    tol = max(abs((mean + a - 0.5) / stats.norm.ppf((ch[dk] + b) / (ch[dk] + ch["R"] + b - b2)) / isd - 1.0)
                              for a in (-ROUND, ROUND) for b in (-5e-6, 5e-6) for b2 in (-5e-6, 5e-6)) + TOL_DENSITY
                    t_sd.add(tag, isd, sd, tol)
                ctl = blk.get("control")
                if ctl:
                    w = c["stage_two"]["inputs"].get("P_decides_given_tie")
                    t_ctl.add(tag, blk["value"] * w, ctl["value"], 1e-12)
                    t_ctl.add(tag + " event", 2 * ctl["value"], ctl["event"], 0.0)
                if blk is p and (n * sd * sd < 200 or rng.random() < 0.01):
                    exact_rows.append((c["id"], n, mean, sd, tails, fh / (2 * n)))
    print(f"  contests: {n_p} with p > 0, {n_zero} with p = 0, {n_nop} not computed")
    print(f"  not computed without a reason: {nop_without_reason or 'none'}; p = 0 without a reason: "
          f"{zero_without_reason or 'none'}")
    print(f"  p > 0 lacking under/computed_by/commit: {unnamed or 'none'}; p = 0 lacking computed_by or commit: "
          f"{len(zero_unnamed)} (e.g. {zero_unnamed[:3]})")
    print(f"  p blocks whose 'under' names no forecast in the contest: {unmatched or 'none'}")
    report("f(1/2) from the recorded (six-decimal) mean and sd (tolerance: the rounding bound of each contest)", t_fh)
    print(f"     largest difference as a share of its rounding bound: {max(share_of_bound)[0]:.3f} ({max(share_of_bound)[1]})")
    report("p = f(1/2) / (2n) (tolerance: the same bound)", t_p)
    report("event = 2 p (exact)", t_event)
    report("538: implied sd = (mean - 1/2) / Phi^-1(D chance / (D + R chances)) (tolerance: the rounding bound of each entry)", t_sd)
    report("control p = seat p x P(decides | tie) as recorded (exact)", t_ctl)
    print(f"  method recorded against the model's rule (exact below n = 1,000 or n sd^2 = 6.25): "
          f"{len(method_wrong)} differ" + (f": {method_wrong[:5]}" if method_wrong else ""))
    # the exact sum against the density form where the data come nearest the switch, and a 1% sample
    exact_rows.sort(key=lambda r: r[1] * r[3] ** 2)
    print(f"  exact lattice sum vs density form, the {min(len(exact_rows), 12)} contests nearest the switch "
          "(smallest n sd^2) and a sample:")
    worst = 0.0
    for cid, n, mean, sd, tails, pd in exact_rows[:12] + exact_rows[12::max(1, len(exact_rows[12:]) // 8)]:
        pe = L.p_exact(n, mean, sd, tails)
        worst = max(worst, abs(pd / pe - 1))
        print(f"     {cid:<28} n {n:>9,} mean {mean:.4f} sd {sd:.4f} n sd^2 {n * sd * sd:8.1f} "
              f"density {pd:.6e} exact {pe:.6e} ratio {pd / pe:.6f}")
    print(f"  largest |density / exact - 1| over these: {worst:.2e}")


def main():
    print("C1. EVERY p RECOMPUTED FROM ITS OWN INPUTS (M2's code; no pipeline import)")
    print(f"repository HEAD {L.git_head()}")
    check_president()
    for level in ("senate", "house", "governor"):
        check_congress(level)


if __name__ == "__main__":
    main()
