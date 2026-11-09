# AAE1001 Group 3 Project Report — Aircraft Route & Cost Optimisation

> **Course:** AAE1001 Introduction to Artificial Intelligence and Data Analytics in Aerospace and Aviation Engineering
> **Repository:** `AAE1001_26_Group_3`
> **Challenge map:** Group 3 obstacle set (Week 8 lecture slides)
> **Semester:** 2026/27

![Task 1 result](Task1/Task1_Sc1.png)
*Figure 0 — Group 3 fastest path found by our A\* implementation (T_best = 94.90 min).*
![Git history](images/git-history.png)

*Figure 4 — Commit history of the group repository. Five branches
were merged into main; each merge node marks an integrated task.*
---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Repository Structure](#2-repository-structure)
3. [Environment & How to Run](#3-environment--how-to-run)
4. [Task 1 — Fastest Path & Minimum-Cost Aircraft per Scenario](#4-task-1--fastest-path--minimum-cost-aircraft-per-scenario)
5. [Task 2 — Jet Stream (Cost-Area) Design](#5-task-2--jet-stream-cost-area-design)
6. [Task 3 — New Aircraft Design](#6-task-3--new-aircraft-design)
7. [Additional Task A1 — Supply-Drop Checkpoints](#7-additional-task-a1--supply-drop-checkpoints)
8. [Additional Task A2 — Randomised Environment](#8-additional-task-a2--randomised-environment)
9. [Additional Task A3 — Algorithm Comparison](#9-additional-task-a3--algorithm-comparison)
10. [Group Contributions](#10-group-contributions)
11. [GenAI Usage Disclosure](#11-genai-usage-disclosure)
12. [Individual Reflective Essays](#12-individual-reflective-essays)

---

## 1. Project Overview

The project plans aircraft routes on a 2-D integer grid (coordinates −10 … 60 on both axes) that contains each group's own obstacle set, a **fuel-consuming area** and a **time-consuming area**. Movement costs one minute per orthogonal grid step and two minutes per diagonal step; inside a cost-intensive area the flight time of the step is inflated (we use **+15 % in the fuel-consuming area** and **+30 % in the time-consuming area**, following the Week 8 rule *"30 % and 15 % additional flight time for cost intensive area for Time and Fuel"*).

The trip cost of one flight follows the lecture equation

```
cost_per_flight = C_F · (fuel rate kg/min) · T + C_T · T + C_c
total_cost      = cost_per_flight · number_of_flights
```

with `T` = best trip time returned by the path planner, and `number_of_flights = ceil(passengers / capacity)`, capped by the scenario limit.

Every task is implemented in **its own `.py` file** (as required), and all results reported below were produced by running those files on the Group 3 map.

---

## 2. Repository Structure

```
AAE1001_26_Group_3/
├── README.md                          # this report
├── code/
│   ├── task1_cost_model.py            # Task 1: A* + scenario cost comparison
│   ├── task2_jetstream.py             # Task 2: jet-stream band optimisation
│   ├── task3_aircraft_design.py       # Task 3: new-aircraft parameter design
│   ├── taskA1_checkpoints.py          # A1: two supply-drop checkpoints
│   ├── taskA2_random_environment.py   # A2: random environment generator
│   └── taskA3_algorithm_comparison.py # A3: Dijkstra vs A* vs Greedy
└── results/
    ├── task1_group3.png
    ├── task2_group3_jetstream.png
    ├── taskA1_group3.png
    ├── taskA2_seed3.png
    └── taskA3_group3.png
```

---

## 3. Environment & How to Run

| Item | Value |
| --- | --- |
| Python | 3.10+ |
| Dependencies | standard library only for computation; `matplotlib` for plotting |
| Install plotting | `pip install matplotlib` |

Run any task from the `code/` directory:

```bash
python task1_cost_model.py --group 3 --plot        # Task 1
python task2_jetstream.py  --group 3 --plot        # Task 2
python task3_aircraft_design.py --group 3         # Task 3
python taskA1_checkpoints.py --group 3            # Additional task A1
python taskA2_random_environment.py --seed 3      # Additional task A2
python taskA3_algorithm_comparison.py --group 3   # Additional task A3
```

All scripts accept `--group 1..12`, so the same code base serves every group map.

---

## 4. Task 1 — Fastest Path & Minimum-Cost Aircraft per Scenario

**Method.** A\* searches the grid with step cost = (1 or 2 minutes) × area factor; the Manhattan distance is used as an admissible heuristic. The returned `T_best` is then fed into the cost equation for the three aircraft (A321neo, A330-900neo, A350-900) under each scenario's time-cost level and fuel price.

**Group 3 result: T_best = 94.90 minutes** (see Figure 0 above — the planner hugs the obstacle wall at x = 30 and cuts through the corner of the time-consuming area, which is cheaper than a longer detour).

| Scenario | Passengers / flight cap | Time & fuel cost | A321neo | A330-900neo | A350-900 | **Optimum** |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 3300 / ≤13 | medium, 0.85 $/kg | infeasible | 11 fl · $118,456 | 10 fl · $123,222 | **A330-900neo × 11** |
| 2 | 1500 / ≤7 | high, 0.96 $/kg | infeasible | 5 fl · $61,075 | 5 fl · $69,630 | **A330-900neo × 5** |
| 3 | 2250 / ≤25 | low, 0.78 $/kg | 12 fl · $80,954 | 8 fl · $77,131 | 7 fl · $77,420 | **A330-900neo × 8** |

*Discussion.* In Scenarios 1 and 2 the A321neo cannot satisfy the passenger demand within the flight cap, so the choice is between A330 and A350; the A330's lower fuel burn (84 vs 90 kg/min) and lower time cost win in both. In Scenario 3 all three are feasible and the answer is close: the A330's extra flight is cheaper than the A350's higher per-flight cost, so the A330 wins by $289 only — a good illustration of the fixed-cost / variable-cost trade-off.



## 5. Task 2 — Jet Stream (Cost-Area) Design

**Method.** A jet stream is a horizontal band, five units tall, spanning the full map width, in which every step cost is multiplied by 0.95. `task2_jetstream.py` enumerates all 67 legal band positions, re-runs A\* for each, and ranks them by Scenario 1 total cost.

**Group 3 optimum: band y = 19 … 23.**

| Case | T_best (min) | Scenario 1 minimum total cost |
| --- | --- | --- |
| No jet stream (baseline) | 94.90 | $118,456 |
| **Jet stream y = 19–23** | **92.91** | **$116,429** |

Saving: **$2,028 (1.71 %)** per weekly operation of Scenario 1.

![Jet stream](Task2/Task2.png)
*Figure 1 — Optimal jet stream (cyan band). It is placed exactly where the fastest path squeezes between the obstacle wall and the time-consuming area, so the discounted cells lie on the route instead of in empty space.*

---

## 6. Task 3 — New Aircraft Design

**Rules applied** (Week 8 slides): capacity 100–450 in steps of 50; base C_T = 12 $/min plus 2 $/min per 50 passengers; twin-engine below 300 seats, four engines from 300 seats; C_c = 2000 (twin) / 2500 (four); each engine burns 20 kg/min; evaluated on Scenario 1 with T_best = 94.90 min.

| Design | Cap | Engines | Rate (kg/min) | C_T | C_c | Flights | Total cost |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AeroStream-100T … 250T | 100–250 | 2 | 40 | 12–18 | 2000 | >13 | infeasible |
| AeroStream-300Q | 300 | 4 | 80 | 20 | 2500 | 11 | $119,363 |
| AeroStream-350Q | 350 | 4 | 80 | 22 | 2500 | 10 | $110,410 |
| AeroStream-400Q | 400 | 4 | 80 | 24 | 2500 | 9 | $101,077 |
| **AeroStream-450Q** | **450** | **4** | **80** | **26** | **2500** | **8** | **$91,365** |

**Chosen design: AeroStream-450Q** — 450 passengers, four engines, 80 kg/min, C_T = 26 $/min, C_c = $2,500, eight flights, total **$91,365**, i.e. **$27,091 cheaper** than the best existing aircraft (A330-900neo, $118,456).

*Reasoning behind the rules (open-ended bonus):* larger capacity amortises the fixed cost C_c over fewer flights, which is why total cost falls monotonically with capacity; the ≥300-seat four-engine rule models thrust/redundancy requirements and doubles the fuel rate, which is why the 300-seat design is *more* expensive per flight than a 250-seat twin would be — but small twins are ruled out by the 13-flight cap. The optimum therefore sits at the largest capacity the constraint set allows.

---

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

---

## 9. Additional Task A3 — Algorithm Comparison

Two further algorithms were taken from the [PythonRobotics](https://github.com/AtsushiSakai/PythonRobotics) repository (`PathPlanning/Dijkstra`, `PathPlanning/GreedyBestFirstSearch`) and unified with our A\* in one best-first framework that differs only in the priority `f(n)`: Dijkstra `f = g`, A\* `f = g + h`, Greedy `f = h`. All three run on the **same** Group 3 obstacle set and cost model.

| Algorithm | T (min) | Path length | Nodes expanded | Wall time | Optimal? |
| --- | --- | --- | --- | --- | --- |
| Dijkstra | 94.90 | 64 | 4343 | 10.6 ms | yes |
| **A\*** | **94.90** | **64** | **1766** | **3.6 ms** | **yes** |
| Greedy best-first | 94.90 | 67 | 624 | 1.4 ms | yes (on this map) |

![Algorithm comparison Mapversion](AddionalTaskA/TaskA3(1).png)
![AlgorithmComparison2](AddionalTaskA/TaskA3(2).png)
*Figure 4 — The three routes on the identical obstacle set.*

*Discussion.* Dijkstra expands nodes in every direction because it has no heuristic: it is provably optimal but the slowest and most memory-hungry. A\* keeps the same optimal cost while expanding ~59 % fewer nodes thanks to the admissible Manhattan heuristic — the best trade-off here. Greedy is by far the fastest (624 nodes) and happens to reach the optimum on the Group 3 map, but this is luck, not a guarantee: ignoring the cost already paid, it is trapped by cost areas on other maps — over all twelve group maps it is optimal on only 3, while Dijkstra and A\* are optimal on 12/12 (average T: Dijkstra 84.17, A\* 84.17, Greedy 87.08 min). Conclusion: use A\* when an admissible heuristic is available, Dijkstra when none is, and Greedy only when speed matters more than cost.

---

## 10. Group Contributions

| Member (name / student ID) | Main responsibility |
| --- | --- |
| Member 1 — *[fill in]* | Task 1 A\* core, repository setup |
| Member 2 — *[fill in]* | Task 2 jet stream, results collection |
| Member 3 — *[fill in]* | Task 3 aircraft design, cost tables |
| Member 4 — *[fill in]* | Additional tasks A1–A3, plots |
| Member 5 — *[fill in]* | README report, presentation slides |
| Member 6 — *[fill in]* | ？|
| Member 7 — *[fill in]* | ？|
| Member 8 — *[fill in]* | ？|

*(Adjust the rows to your actual team; commit history backs up the split of work.)*

---

## 11. GenAI Usage Disclosure

A generative AI assistant was used as a coding partner: it helped draft and debug the A\* / comparison implementations, generate the plotting code and structure this README. **All numbers in this report were produced by running the committed scripts**, and every design decision (cost factors, checkpoint placement, jet-stream ranking) was reviewed and accepted by the group members.

---

## 12. Individual Reflective Essays

> Each member contributes 200–250 words below, in first person, reflecting on their own learning during this project (what they found hard, what they changed their mind about, what they would do differently).

### Member 1 — *[name]*

*[200–250 words]*

### Member 2 — *[name]*

*[200–250 words]*

### Member 3 — *[name]*

*[200–250 words]*

### Member 4 — *[name]*

*[200–250 words]*

### Member 5 — *[name]*

*[200–250 words]*

### Member 6 — *[name]*

*[200–250 words]*

### Member 7 — *[name]*

*[200–250 words]*

### Member 8 — *[name]*

*[200–250 words]*

---

*Report generated from the committed code; re-run any script above to reproduce every figure and number.*
