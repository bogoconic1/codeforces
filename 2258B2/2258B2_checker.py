#!/usr/bin/env python3
"""Brute-force stress checker for CF 2258 B2 - Carrot Chopdown (Hard Version).

The brute force *simulates the machine* (every x, every subset of carrots,
exactly k operations), so it validates the per-carrot formula as well as
the counting code.

Usage:
  python3 2258B2_checker.py --num-cases 200 --max-n 3 --max-m 6
  python3 2258B2_checker.py --samples          # verify brute vs official samples
  python3 2258B2_checker.py --solution other.py --seed 7 --interp pypy3
"""
import argparse, random, subprocess, sys, os
from collections import Counter
from functools import lru_cache

SOLUTION = os.path.join(os.path.dirname(os.path.abspath(__file__)), "B_2_Carrot_Chopdown_Hard_Version.py")

# ---------------- brute force ----------------
@lru_cache(None)
def best(state, k):
    """state: sorted tuple of carrot lengths; max #equal-length carrots after exactly k ops."""
    if k == 0:
        return max(Counter(state).values())
    res = best(state, k - 1)  # choose the empty set: nothing changes
    mx = max(state)
    for x in range(1, mx):
        idx = [i for i, l in enumerate(state) if l > x]
        for mask in range(1, 1 << len(idx)):
            new = list(state)
            add = []
            for b, i in enumerate(idx):
                if mask >> b & 1:
                    new[i] = x
                    add.append(state[i] - x)
            res = max(res, best(tuple(sorted(new + add)), k - 1))
    return res

def brute(inp):
    data = inp.split(); pos = 0
    t = int(data[pos]); pos += 1
    out = []
    for _ in range(t):
        n, m = int(data[pos]), int(data[pos + 1]); pos += 2
        a = tuple(sorted(int(v) for v in data[pos:pos + n])); pos += n
        out.append(" ".join(str(best(a, k)) for k in range(1, m + 1)))
    return "\n".join(out)

# ---------------- generator ----------------
def gen(rng, a):
    t = rng.randint(1, a.max_t)
    lines = [str(t)]
    for _ in range(t):
        n = rng.randint(1, a.max_n)
        m = rng.randint(1, a.max_m)
        lines.append(f"{n} {m}")
        lines.append(" ".join(str(rng.randint(1, m)) for _ in range(n)))
    return "\n".join(lines) + "\n"

SAMPLE_IN = """6
5 4
1 2 3 4 4
5 8
1 1 8 8 8
1 8
6
7 9
1 7 5 1 7 5 3
4 1
1 1 1 1
3 5
3 1 5
"""
SAMPLE_OUT = """6 14 14 14
6 12 26 26 26 26 26 26
2 3 6 6 6 6 6 6
7 17 29 29 29 29 29 29 29
4
3 7 9 9 9"""

# ---------------- runner ----------------
def run_solution(cmd, inp):
    r = subprocess.run(cmd, input=inp, capture_output=True, text=True)
    if r.returncode != 0:
        return None, r.stderr
    return r.stdout, ""

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--num-cases", type=int, default=200)
    p.add_argument("--max-t", type=int, default=3)
    p.add_argument("--max-n", type=int, default=3)
    p.add_argument("--max-m", type=int, default=6)
    p.add_argument("--seed", type=int, default=None)
    p.add_argument("--solution", default=SOLUTION)
    p.add_argument("--interp", default=sys.executable, help="interpreter for solution (e.g. pypy3)")
    p.add_argument("--samples", action="store_true", help="only check brute against samples")
    a = p.parse_args()

    if a.samples:
        got = brute(SAMPLE_IN).split()
        exp = SAMPLE_OUT.split()
        print("brute:", got, "expected:", exp, "OK" if got == exp else "FAIL")
        return

    rng = random.Random(a.seed)
    cmd = [a.interp, a.solution]
    for it in range(1, a.num_cases + 1):
        inp = gen(rng, a)
        exp = brute(inp).split()
        got, err = run_solution(cmd, inp)
        if got is None or got.split() != exp:
            print(f"MISMATCH on case {it}")
            print("--- input ---"); print(inp, end="")
            print("--- expected ---"); print(" ".join(exp))
            print("--- got ---"); print(got.strip() if got is not None else "RUNTIME ERROR:\n" + err)
            sys.exit(1)
    print(f"all {a.num_cases} cases passed")

if __name__ == "__main__":
    main()
