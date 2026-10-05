import random
import numpy as np
import matplotlib.pyplot as plt
import math

# ==========================================
# 1. GENERATE UNIQUE PROBLEM INSTANCE
# ==========================================
ROLL_NUMBER = 91  # Muhammad Danish: Replace with your actual numerical roll number
random.seed(ROLL_NUMBER)
np.random.seed(ROLL_NUMBER)

GRID_SIZE = 20
NUM_OBSTACLES = 60 # Roughly 15% of the 20x20 grid

# Generate Obstacles
obstacles = set()
while len(obstacles) < NUM_OBSTACLES:
    x, y = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
    obstacles.add((x, y))

# Generate Start and Goal (must not be obstacles and must not be the same)
def get_free_cell():
    while True:
        cell = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
        if cell not in obstacles:
            return cell

start_point = get_free_cell()
goal_point = get_free_cell()
while goal_point == start_point:
    goal_point = get_free_cell()

print(f"Seed: {ROLL_NUMBER}")
print(f"Start: {start_point}, Goal: {goal_point}")

# ==========================================
# 2. PSO ALGORITHM SETUP
# ==========================================
NUM_PARTICLES = 50
ITERATIONS = 100
NUM_WAYPOINTS = 5 # Intermediate points between start and goal

# PSO Parameters
W = 0.5    # Inertia
C1 = 1.5   # Cognitive (Personal Best)
C2 = 1.5   # Social (Global Best)

# Initialize particles (each particle is a flattened array of x,y coordinates for waypoints)
# Bounds are 0 to GRID_SIZE - 1
particles = np.random.uniform(0, GRID_SIZE-1, (NUM_PARTICLES, NUM_WAYPOINTS * 2))
velocities = np.zeros((NUM_PARTICLES, NUM_WAYPOINTS * 2))
pbest_positions = np.copy(particles)
pbest_scores = np.full(NUM_PARTICLES, np.inf)
gbest_position = None
gbest_score = np.inf

# ==========================================
# 3. FITNESS & COLLISION CHECKING
# ==========================================
def check_collision(p1, p2):
    """Samples points along a line segment to check for obstacle collisions."""
    steps = int(max(abs(p2[0]-p1[0]), abs(p2[1]-p1[1]))) * 2 + 2
    for i in range(steps):
        t = i / max(steps - 1, 1)
        x = int(round(p1[0] + t * (p2[0] - p1[0])))
        y = int(round(p1[1] + t * (p2[1] - p1[1])))
        if (x, y) in obstacles:
            return True
        if x < 0 or x >= GRID_SIZE or y < 0 or y >= GRID_SIZE:
            return True # Out of bounds is treated as a collision
    return False

def calculate_fitness(particle):
    points = [start_point] + [(particle[i], particle[i+1]) for i in range(0, len(particle), 2)] + [goal_point]
    distance = 0
    penalty = 0
    
    for i in range(len(points)-1):
        p1 = points[i]
        p2 = points[i+1]
        distance += math.hypot(p2[0]-p1[0], p2[1]-p1[1])
        
        # Heavy penalty if the path segment crosses an obstacle
        if check_collision(p1, p2):
            penalty += 1000 
            
    return distance + penalty

# ==========================================
# 4. MAIN PSO LOOP
# ==========================================
"""for iteration in range(ITERATIONS):
    for i in range(NUM_PARTICLES):
        fitness = calculate_fitness(particles[i])
        
        # Update Personal Best
        if fitness < pbest_scores[i]:
            pbest_scores[i] = fitness
            pbest_positions[i] = particles[i]
            
        # Update Global Best
        if fitness < gbest_score:
            gbest_score = fitness
            gbest_position = np.copy(particles[i])
            
    # Update Velocities and Positions
    for i in range(NUM_PARTICLES):
        r1, r2 = np.random.rand(), np.random.rand()
        velocities[i] = (W * velocities[i] + 
                         C1 * r1 * (pbest_positions[i] - particles[i]) + 
                         C2 * r2 * (gbest_position - particles[i]))
        particles[i] += velocities[i]
        
        # Keep particles within grid bounds
        particles[i] = np.clip(particles[i], 0, GRID_SIZE-1)

# ==========================================
# 5. VISUALIZATION
# ==========================================
best_path_points = [start_point] + [(gbest_position[i], gbest_position[i+1]) for i in range(0, len(gbest_position), 2)] + [goal_point]
print(f"Best Path Cost/Length: {gbest_score:.2f}")

fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(-0.5, GRID_SIZE-0.5)
ax.set_ylim(-0.5, GRID_SIZE-0.5)
ax.set_xticks(np.arange(GRID_SIZE))
ax.set_yticks(np.arange(GRID_SIZE))
ax.grid(True, linestyle=':', color='gray', alpha=0.6)

# Plot Obstacles
obs_x = [o[0] for o in obstacles]
obs_y = [o[1] for o in obstacles]
ax.scatter(obs_x, obs_y, c='black', marker='s', s=100, label='Obstacles')

# Plot Start and Goal
ax.scatter(*start_point, c='blue', marker='s', s=150, label='Start')
ax.scatter(*goal_point, c='green', marker='s', s=150, label='Goal')

# Plot Best Path
path_x = [p[0] for p in best_path_points]
path_y = [p[1] for p in best_path_points]
ax.plot(path_x, path_y, c='red', linewidth=2.5, marker='o', label='PSO Best Path')

plt.title(f"PSO Path Planning (Seed: {ROLL_NUMBER})")
plt.legend(loc='upper right')
plt.gca().invert_yaxis() # Match standard grid/matrix visualization
plt.show() 
""""