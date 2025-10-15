# Convex Hull — Divide and Conquer Implementation
##  Overview
The algorithm works in **O(n log n)** time by:
1. Sorting all points by their x-coordinate (and y-coordinate for ties).
2. Recursively dividing the point set into two halves.
3. Computing the convex hull of each half.
4. Merging the two convex hulls using *upper* and *lower* tangents.
##  How It Works
1. **Divide:**  
   Sort all input points by x-coordinate (and y-coordinate as a tiebreaker), then split the list into two halves.
2. **Conquer:**  
   Recursively compute the convex hull of each half.
3. **Merge:**  
   Connect the two hulls by finding upper and lower tangents and combining the two halves.

The overall time complexity is **O(n log n)**.
##  Main Fuction
| Function              | Description                                                 |
| --------------------- | ----------------------------------------------------------- |
| `orient(a, b, c)`     | Computes turn direction (positive = left turn).             |
| `trivial_hull(pts)`   | Builds a small hull directly (≤3 points).                   |
| `merge(HL, HR)`       | Merges left and right hulls using upper and lower tangents. |
| `dch(sorted_pts)`     | Recursive divide-and-conquer core.                          |
| `convex_hull(points)` | Main entry: sorts points and computes hull.                 |
| `time_once(n)`        | Measures time for one convex hull computation.              |
| `time_median(n)`      | Runs multiple trials and takes the median runtime.          |
##  Finding Extreme Points
```
def rightmost(h: List[Point]) -> int:
    return max(range(len(h)), key=lambda i:(h[i][0], h[i][1]))

def leftmost(h: List[Point]) -> int:
    return min(range(len(h)), key=lambda i:(h[i][0], h[i][1]))

##  Merging Two Hulls
```
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
  ```
##  Divide and Conquer
```
def dch(sorted_pts: List[Point]) -> List[Point]:
    n = len(sorted_pts)
    if n <= 3: return trivial_hull(sorted_pts)
    mid = n // 2
    return merge(dch(sorted_pts[:mid]), dch(sorted_pts[mid:]))
    ```
