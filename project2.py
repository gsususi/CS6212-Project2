"""
Author:Lanbin Wang
"""
from typing import List, Tuple
import random, time, math, statistics

Point = Tuple[float, float]
def orient(a: Point, b: Point, c: Point) -> float:
    # Returns the signed area * 2 of triangle (a, b, c)
    return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])
def trivial_hull(pts: List[Point]) -> List[Point]:
    s = sorted(set(pts))
    if len(s) <= 2:
        return s                      # 0–2 points: the hull is itself
    a, b, c = s
    t = orient(a, b, c)
    if t > 0:  return [a, b, c]       # counterclockwise triangle
    if t < 0:  return [a, c, b]       # clockwise triangle
    return [a, c]                     # collinear: keep endpoints only
def rightmost(h: List[Point]) -> int:
    return max(range(len(h)), key=lambda i: (h[i][0], h[i][1]))
def leftmost(h: List[Point]) -> int:
    return min(range(len(h)), key=lambda i: (h[i][0], h[i][1]))
def merge(HL: List[Point], HR: List[Point]) -> List[Point]:   # Merge two convex hulls
    nL, nR = len(HL), len(HR)
    i, j = rightmost(HL), leftmost(HR)

    changed = True              # Find upper tangent
    while changed:
        changed = False
        while orient(HL[i], HR[j], HR[(j+1)%nR]) > 0:    # Move right hull point upward
            j = (j+1) % nR; changed = True
        while orient(HR[j], HL[i], HL[(i-1)%nL]) < 0:     # Move left hull point upward
            i = (i-1) % nL; changed = True
    iu, ju = i, j  # upper tangent endpoints

    i, j = rightmost(HL), leftmost(HR)            # Find lower tangent
    changed = True
    while changed:
        changed = False
        while orient(HL[i], HR[j], HR[(j-1)%nR]) < 0:    # Move right hull point downward
            j = (j-1) % nR; changed = True
        while orient(HR[j], HL[i], HL[(i+1)%nL]) > 0:    # Move left hull point downward
            i = (i+1) % nL; changed = True
    il, jl = i, j  # lower tangent endpoint

    H = []     # Combine
    k = iu
    H.append(HL[k])
    while k != il:
        k = (k+1) % nL
        H.append(HL[k])
    k = jl
    H.append(HR[k])
    while k != ju:
        k = (k+1) % nR
        H.append(HR[k])

    if len(H) <= 2:
        return H
    R = []
    m = len(H)
    for t in range(m):
        if orient(H[(t-1)%m], H[t], H[(t+1)%m]) != 0:
            R.append(H[t])
    # Return reduced hull or fallback to endpoints
    return R or [min(H), max(H)]

def dch(sorted_pts: List[Point]) -> List[Point]:
    n = len(sorted_pts)
    if n <= 3:
        return trivial_hull(sorted_pts)
    mid = n // 2
    # Recursively build hulls and merge them
    return merge(dch(sorted_pts[:mid]), dch(sorted_pts[mid:]))
def convex_hull(points: List[Point]) -> List[Point]:       # Main convex hull entry
    pts = sorted(set(points))          #  global sort by (x, y)
    if len(pts) <= 3:
        return trivial_hull(pts)
    return dch(pts)                    # Conquer and merge recursively
def gen_points(n: int, seed: int) -> List[Point]:
    rnd = random.Random(seed)
    return [(rnd.random(), rnd.random()) for _ in range(n)]
def time_once_ms(n: int, seed: int = 12345) -> float:   # Measure single run time
    pts = gen_points(n, seed)
    t0 = time.perf_counter_ns()
    _ = convex_hull(pts)
    t1 = time.perf_counter_ns()
    return (t1 - t0) / 1e6             # Convert to milliseconds
def time_median_ms(n: int, trials: int = 3, seed_base: int = 1000) -> float:
    samples = [ time_once_ms(n, seed_base + k) for k in range(trials) ]
    return statistics.median(samples)

if __name__ == "__main__":
    N = [200, 500, 1000, 2000, 5000, 10000, 20000]
    print(f"{'n':>8} | {'Experimental_ms':>15} | {'theory n*log2(n)':>16}")
    print("-"*52)
    for n in N:
        exp_ms = time_median_ms(n, trials=3)
        theory = n * math.log(n, 2)
        print(f"{n:8d} | {exp_ms:15.4f} | {theory:16}")