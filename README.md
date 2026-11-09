## 7. Additional Task A1 — Supply-Drop Checkpoints

One checkpoint is generated **inside each cost-intensive area** (area centre, or the nearest free cell of the same area if the centre is blocked); the route is planned segment-by-segment with A\* over `start → CP → CP → goal`, and both visiting orders are evaluated.

**Group 3 result**

| Checkpoint | Cell | Inside |
| --- | --- | --- |
| CP1 | (2, 25) | fuel-consuming area |
| CP2 | (25, 7) | time-consuming area |

Chosen order: `start → CP1 → CP2 → goal`, legs 46.35 + 44.00 + 61.50 min, **total T = 151.85 min**.

![Checkpoints](AddionalTaskA/TaskA1.png)
*Figure 2 — Planned supply route through both checkpoints (magenta diamonds); all drop-offs happen before the aircraft reaches base.*

---

## 8. Additional Task A2 — Randomised Environment

Each run generates a fresh mission. Implementation ↔️ slide requirement:

| # | Requirement | Implementation | Verified |
| --- | --- | --- | --- |
| 1 | only fuel area, random, fixed 40×40 | `AREA_SIZE = 40`, random top-left corner | PASS |
| 2 | diagonal movement disabled, one grid per move | `ALLOW_DIAGONAL = False`, `STEP_COST = 1.0` | PASS |
| 3 | obstacles random, reasonable density | interior density 0.15 (border ring kept) | PASS |
| 4 | random start & goal, ≥40 units apart | rejection sampling on Euclidean distance | PASS |
| 5 | area plot must not cover obstacles; no obstacle at/near start & goal | obstacles drawn above the area (`zorder`); 3-cell clearance around both | PASS |

Example mission (`--seed 3`, fully reproducible): start (−6, 52), goal (47, 24), fuel area (7, 4)–(46, 43), interior density 0.140, start–goal distance 59.9, clearance 4, **T = 83.70 min**; the script prints a PASS/FAIL line for every requirement, and re-samples automatically if a mission has no feasible path.

![Random mission](AddionalTaskA/TaskA2.png)
*Figure 3 — Random mission, seed 3: yellow fuel area, black obstacles drawn on top, red planned path.*
