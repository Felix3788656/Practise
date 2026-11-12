

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



