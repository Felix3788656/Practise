## Task 2

*Task 2.py* (Jet Stream Optimization): Iteratively tests horizontal 5-unit-tall jet stream bands across the airspace to identify the latitude that yields the maximum travel time/cost reduction (-5% cost penalty). Exports task_2_jetstream.gif.

## Additional Task A1 — additional Checkpoints

A checkpoint is randomly generated **inside each cost-intensive area** which means every time the location of checkpoints are different ; the route is decided by A* algorithm, The path should follow `start → CP → CP → goal`.

** result**

| Checkpoint | coordination | Inside |
| --- | --- | --- |
| CP1 | (random in the area) | fuel-consuming area |
| CP2 | (random in the area) | time-consuming area |

Chosen order: `start → CP2 → CP1 → goal`, **total time 100(for example) .

![Checkpoints](task_a1_route.gif)


---

## Additional Task A2 — Changing Environment

Each time there will be a new path as the environment keep changing for each operation.



### 1. Random fuel area

A square fuel-consuming area is placed randomly within the world. Its dimensions are fixed at **40 × 40** grid units.

The program creates the fuel-area coordinate lists, `fc_x` and `fc_y`, and passes them to the A* planner.

### 2. Random start and goal

The start and goal positions are selected randomly inside the world. The goal is repeatedly reselected until its Euclidean distance from the start is at least **40 units**.

### 3. Random obstacles and boundary walls

The program creates boundary walls along all four edges of the world. It then randomly places interior obstacles.

An interior obstacle is rejected if it is closer than `SAFE_DISTANCE` to either the start or the goal. A Python `set` is used to prevent duplicate obstacle coordinates.

| Requirement  | main additional code | 
| --- | --- | 
| Generated only fuel area randomly with a fixed size of 40 × 40 |  (1)  WORLD_MIN, WORLD_MAX = -10, 60 FUEL_AREA_SIZE = 40         (2)   fx = random.randint(WORLD_MIN, WORLD_MAX - FUEL_AREA_SIZE)    fy = random.randint(WORLD_MIN, WORLD_MAX - FUEL_AREA_SIZE)   |  
| Disable diagonal movement and allow movement of one grid per move  | planner.motion = [[1, 0, 1], [0, 1, 1], [-1, 0, 1], [0, -1, 1]] | 
|Generate obstacles randomly with reasonable density while keeping the boundary ring | obstacles = set() for i in range(WORLD_MIN, WORLD_MAX + 1):    obstacles.add((i, WORLD_MIN))  obstacles.add((i, WORLD_MAX)) obstacles.add((WORLD_MIN, i))  obstacles.add((WORLD_MAX, i)) |
| Generate random start and goal positions at least 40 units apart | sx, sy = random.randint(WORLD_MIN + 2, WORLD_MAX - 2), random.randint(WORLD_MIN + 2, WORLD_MAX - 2) gx, gy = random.randint(WORLD_MIN + 2, WORLD_MAX - 2), random.randint(WORLD_MIN + 2, WORLD_MAX - 2) while math.hypot(sx - gx, sy - gy) < 40:    gx, gy = random.randint(WORLD_MIN + 2, WORLD_MAX - 2), random.randint(WORLD_MIN + 2, WORLD_MAX - 2) |




