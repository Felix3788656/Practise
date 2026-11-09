"""Group 11 - Task A3: A* and Bidirectional A* on a shared map."""
import math
import random
import heapq
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# -------------------- ENVIRONMENT SETTINGS --------------------
WORLD_MIN, WORLD_MAX = -10, 60
FUEL_AREA_SIZE = 40
OBSTACLE_COUNT = 1250
SAFE_DISTANCE = 5
RANDOM_SEED = 42
ROBOT_RADIUS = 0.5

def generate_environment():
    rng = random.Random(RANDOM_SEED)
    fx = rng.randint(WORLD_MIN, WORLD_MAX - FUEL_AREA_SIZE)
    fy = rng.randint(WORLD_MIN, WORLD_MAX - FUEL_AREA_SIZE)
    fuel_cells = {(x, y) for x in range(fx, fx + FUEL_AREA_SIZE) for y in range(fy, fy + FUEL_AREA_SIZE)}

    sx = rng.randint(WORLD_MIN + 2, WORLD_MAX - 2)
    sy = rng.randint(WORLD_MIN + 2, WORLD_MAX - 2)
    gx = rng.randint(WORLD_MIN + 2, WORLD_MAX - 2)
    gy = rng.randint(WORLD_MIN + 2, WORLD_MAX - 2)
    while math.hypot(sx - gx, sy - gy) < 40:
        gx = rng.randint(WORLD_MIN + 2, WORLD_MAX - 2)
        gy = rng.randint(WORLD_MIN + 2, WORLD_MAX - 2)

    obstacles = set()
    for i in range(WORLD_MIN, WORLD_MAX + 1):
        obstacles.update({(i, WORLD_MIN), (i, WORLD_MAX), (WORLD_MIN, i), (WORLD_MAX, i)})

    target_count = OBSTACLE_COUNT + 4 * (WORLD_MAX - WORLD_MIN)
    while len(obstacles) < target_count:
        point = (rng.randint(WORLD_MIN + 1, WORLD_MAX - 1), rng.randint(WORLD_MIN + 1, WORLD_MAX - 1))
        if math.hypot(point[0] - sx, point[1] - sy) < SAFE_DISTANCE: continue
        if math.hypot(point[0] - gx, point[1] - gy) < SAFE_DISTANCE: continue
        obstacles.add(point)
    return (fx, fy, fuel_cells, (sx, sy), (gx, gy), obstacles)

# -------------------- COMMON COST / COLLISION RULES --------------------
def step_cost(point): return 2.0 if point in FUEL_CELLS else 1.0
def heuristic(a, b): return abs(a[0] - b[0]) + abs(a[1] - b[1])
MOVES = [(1, 0), (-1, 0), (0, 1), (0, -1)]

def valid_grid_point(p):
    return (WORLD_MIN < p[0] < WORLD_MAX and WORLD_MIN < p[1] < WORLD_MAX and p not in OBSTACLES)

def reconstruct(parent, end):
    path = [end]
    while parent[path[-1]] is not None:
        path.append(parent[path[-1]])
    path.reverse()
    return path

# -------------------- 1. A* --------------------
def astar(start, goal):
    frontier = [(heuristic(start, goal), 0.0, start)]
    g_cost = {start: 0.0}
    parent = {start: None}
    explored = []

    while frontier:
        _, current_cost, current = heapq.heappop(frontier)
        if current_cost != g_cost.get(current): continue
        explored.append(current)
        if current == goal: return reconstruct(parent, goal), explored, current_cost

        for dx, dy in MOVES:
            nxt = (current[0] + dx, current[1] + dy)
            if not valid_grid_point(nxt): continue
            new_cost = current_cost + step_cost(nxt)
            if new_cost < g_cost.get(nxt, math.inf):
                g_cost[nxt] = new_cost
                parent[nxt] = current
                heapq.heappush(frontier, (new_cost + heuristic(nxt, goal), new_cost, nxt))
    return [], explored, math.inf

# -------------------- 2. BIDIRECTIONAL A* --------------------
def bidirectional_astar(start, goal):
    fronts = [[(heuristic(start, goal), 0.0, start)], [(heuristic(goal, start), 0.0, goal)]]
    costs = [{start: 0.0}, {goal: 0.0}]
    parents = [{start: None}, {goal: None}]
    closed = [set(), set()]
    explored = []
    meeting = None

    while fronts[0] and fronts[1]:
        side = 0 if fronts[0][0][0] <= fronts[1][0][0] else 1
        _, g, current = heapq.heappop(fronts[side])
        if g != costs[side].get(current) or current in closed[side]: continue
        closed[side].add(current)
        explored.append(current)

        if current in costs[1 - side]:
            meeting = current
            break

        for dx, dy in MOVES:
            nxt = (current[0] + dx, current[1] + dy)
            if not valid_grid_point(nxt): continue
            ng = g + step_cost(nxt)
            if ng < costs[side].get(nxt, math.inf):
                costs[side][nxt] = ng
                parents[side][nxt] = current
                target = goal if side == 0 else start
                heapq.heappush(fronts[side], (ng + heuristic(nxt, target), ng, nxt))
            if nxt in costs[1 - side]:
                meeting = nxt
                if nxt not in parents[side]: parents[side][nxt] = current
                break
        if meeting is not None: break

    if meeting is None: return [], explored, math.inf

    left = []
    p = meeting
    while p is not None:
        left.append(p)
        p = parents[0].get(p)
    left.reverse()

    right = []
    p = parents[1].get(meeting)
    while p is not None:
        right.append(p)
        p = parents[1].get(p)
    path = left + right
    total = sum(step_cost(p) for p in path[1:])
    return path, explored, total

# -------------------- DRAWING --------------------
def draw_environment(ax, env, title, explored, path):
    fx, fy, _, start, goal, obstacles = env
    ax.add_patch(patches.Rectangle((fx, fy), FUEL_AREA_SIZE, FUEL_AREA_SIZE, facecolor="yellow", edgecolor="black", alpha=0.45, zorder=1))
    ax.scatter([p[0] for p in obstacles], [p[1] for p in obstacles], s=7, c="black", marker="s", zorder=2)
    if explored:
        shown = explored[::max(1, len(explored) // 1200)]
        ax.scatter([p[0] for p in shown], [p[1] for p in shown], s=7, c="deepskyblue", alpha=0.45, zorder=3)
    if path:
        ax.plot([p[0] for p in path], [p[1] for p in path], "-r", linewidth=2.0, zorder=4)
    ax.scatter(*start, marker="*", s=180, c="blue", edgecolors="black", zorder=5)
    ax.scatter(*goal, marker="*", s=180, c="limegreen", edgecolors="black", zorder=5)
    ax.set_xlim(WORLD_MIN - 2, WORLD_MAX + 2)
    ax.set_ylim(WORLD_MIN - 2, WORLD_MAX + 2)
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, linestyle="--", alpha=0.3)
    ax.set_title(title, fontsize=11)

def main():
    global FUEL_CELLS, OBSTACLES
    env = generate_environment()              
    fx, fy, FUEL_CELLS, start, goal, OBSTACLES = env
    
    print("Running A*...")
    path_a, explored_a, cost_a = astar(start, goal)
    print(f"A*: cost={cost_a:.2f} | explored={len(explored_a)}")

    print("Running Bidirectional A*...")
    path_b, explored_b, cost_b = bidirectional_astar(start, goal)
    print(f"Bidirectional A*: cost={cost_b:.2f} | explored={len(explored_b)}")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    draw_environment(ax1, env, f"A* | cost: {cost_a:.1f}", explored_a, path_a)
    draw_environment(ax2, env, f"Bidirectional A* | cost: {cost_b:.1f}", explored_b, path_b)
    
    fig.suptitle("Task A3: A* vs Bidirectional A*", fontsize=15)
    fig.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
