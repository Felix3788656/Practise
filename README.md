import math
import a_star_g11 as a_star_module  # Imports your A* file

# Turn off the animation so it runs quickly in the background
a_star_module.show_animation = False

# ==========================================
# 1. AIRCRAFT DATA (From Slide 5)
# ==========================================
AIRCRAFTS = {
    "A321neo": {
        "fuel_rate": 54, "capacity": 200, "fixed_cost": 1800,
        "time_cost": {"Low": 10, "Medium": 15, "High": 20}
    },
    "A330-900neo": {
        "fuel_rate": 84, "capacity": 300, "fixed_cost": 2000,
        "time_cost": {"Low": 15, "Medium": 21, "High": 27}
    },
    "A350-900": {
        "fuel_rate": 90, "capacity": 350, "fixed_cost": 2500,
        "time_cost": {"Low": 20, "Medium": 27, "High": 34}
    }
}

# ==========================================
# 2. SCENARIOS (From Slide 8)
# ==========================================
SCENARIOS = [
    {"name": "Scenario 1", "passengers": 3300, "max_flights": 13, "time_level": "Medium", "fuel_price": 0.85},
    {"name": "Scenario 2", "passengers": 1500, "max_flights": 7, "time_level": "High", "fuel_price": 0.96},
    {"name": "Scenario 3", "passengers": 2250, "max_flights": 25, "time_level": "Low", "fuel_price": 0.78}
]


def main():
    # --- MAP SETUP ---
    sx, sy = 0.0, 0.0
    gx, gy = 40.0, 50.0
    grid_size = 1
    robot_radius = 1.0

    ox, oy = [], []
    for i in range(-10, 61): ox.append(-10.0); oy.append(i)
    for i in range(-10, 61): ox.append(60.0); oy.append(i)
    for i in range(-10, 61): ox.append(i); oy.append(-10.0)
    for i in range(-10, 61): ox.append(i); oy.append(60.0)
    for i in range(30, 51): ox.append(10.0); oy.append(i)

    # Diagonal walls
    for i in [i * 0.1 for i in range(100, 201)]: ox.append(i); oy.append(-2 * i + 50)
    for i in [i * 0.1 for i in range(200, 301)]: ox.append(i); oy.append(4 * i - 90)

    # Cost Areas
    tc_x, tc_y = [], []  # Time Area
    for i in range(-10, 11):
        for j in range(10, 21): tc_x.append(i); tc_y.append(j)

    fc_x, fc_y = [], []  # Fuel Area
    for i in range(30, 61):
        for j in range(30, 41): fc_x.append(i); fc_y.append(j)

    # --- RUN A* ALGORITHM ---
    print("Calculating fastest route using A*...")
    a_star = a_star_module.AStarPlanner(ox, oy, grid_size, robot_radius, fc_x, fc_y, tc_x, tc_y, sx, sy, gx, gy)

    # Force the penalties to match the assignment rules
    a_star.Delta_C1 = 0.30  # Time Area penalty
    a_star.Delta_C2 = 0.15  # Fuel Area penalty

    # The A* returns three things now: path_x, path_y, and the total cost (time)
    # We don't need the path coordinates here, so we use "_" to ignore them.
    _, _, t_best = a_star.planning(sx, sy, gx, gy)
    print(f"--> Fastest Route Time (T_best): {t_best:.2f} minutes\n")

    # --- EVALUATE SCENARIOS ---
    for s in SCENARIOS:
        print(f"==================================================")
        print(f"{s['name']}: {s['passengers']} Passengers | Max {s['max_flights']} Flights | Time: {s['time_level']} | Fuel: ${s['fuel_price']}/kg")
        print(f"==================================================")

        valid_options = []

        for name, data in AIRCRAFTS.items():
            # 1. Calculate how many flights are needed using math.ceil() to round UP
            flights_needed = math.ceil(s['passengers'] / data['capacity'])

            # 2. Check if it exceeds max flights
            if flights_needed > s['max_flights']:
                print(f"  [X] {name}: Rejected ({flights_needed} flights needed, max is {s['max_flights']})")
                continue

            # 3. Calculate Cost using the Slide 7 formula
            fuel_cost_single = s['fuel_price'] * data['fuel_rate'] * t_best
            time_cost_single = data['time_cost'][s['time_level']] * t_best
            single_trip_cost = fuel_cost_single + time_cost_single + data['fixed_cost']

            # Multiply by the number of flights to get the total fleet cost
            total_fleet_cost = single_trip_cost * flights_needed

            print(f"  [O] {name}: Needs {flights_needed} flights. Total Fleet Cost = ${total_fleet_cost:,.2f}")

            valid_options.append({
                "name": name,
                "flights": flights_needed,
                "total_cost": total_fleet_cost
            })

        # 4. Determine the winner
        if valid_options:
            winner = min(valid_options, key=lambda x: x["total_cost"])
            print(f"\n  ==> BEST AIRCRAFT: {winner['name']} ({winner['flights']} flights, Total Cost: ${winner['total_cost']:,.2f})\n")
        else:
            print("\n  ==> NO AIRCRAFT CAN SATISFY THE REQUIREMENTS\n")


if __name__ == '__main__':
    main()
