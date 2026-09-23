# -*- coding: utf-8 -*-
"""SI Lab_1.ipynb

**Part A**

**Q- What is search space?**

Search space is set of all posible solutions that optimization algorithm can use. The search space consists of possible (x,y) cordinates within a specified range. The function assigns score to each point and our goal is to find the lowest score point.

**Part B**
"""

import numpy as np
import matplotlib.pyplot as plt

def sphere(x,y):
  return x**2 + y**2

x= np.linspace(-5,5,200)
y= np.linspace(-5,5,200)

X,Y = np.meshgrid(x,y)
Z = sphere(X,Y)

plt.contourf(X, Y, Z, levels=30, cmap='viridis')
plt.colorbar(label='f(x,y)')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Sphere Function Contour Plot')
plt.show()

def rastrigin(x, y):
    A = 10
    return 2*A + (x**2 - A*np.cos(2*np.pi*x)) + \
                 (y**2 - A*np.cos(2*np.pi*y))

x = np.linspace(-5.12, 5.12, 200)
y = np.linspace(-5.12, 5.12, 200)

X, Y = np.meshgrid(x, y)
Z = rastrigin(X, Y)

plt.contourf(X, Y, Z, levels=30, cmap='viridis')
plt.colorbar(label='f(x,y)')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Rastrigin Function Contour Plot')
plt.show()

def ackley(x, y):
    return (
        -20 * np.exp(-0.2 * np.sqrt(0.5 * (x**2 + y**2)))
        - np.exp(0.5 * (
            np.cos(2*np.pi*x) +
            np.cos(2*np.pi*y)
        ))
        + np.e + 20
    )

x = np.linspace(-5, 5, 200)
y = np.linspace(-5, 5, 200)

X, Y = np.meshgrid(x, y)
Z = ackley(X, Y)

plt.contourf(X, Y, Z, levels=30, cmap='viridis')
plt.colorbar(label='f(x,y)')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Ackley Function Landscape')
plt.show()

# Ackley Standard Domain Values
def ackley(x, y):
    return (
        -20 * np.exp(-0.2 * np.sqrt(0.5 * (x**2 + y**2)))
        - np.exp(0.5 * (
            np.cos(2*np.pi*x) +
            np.cos(2*np.pi*y)
        ))
        + np.e + 20
    )

x = np.linspace(-32.768, 32.768, 200)
y = np.linspace(-32.768, 32.768, 200)

X, Y = np.meshgrid(x, y)
Z = ackley(X, Y)

plt.contourf(X, Y, Z, levels=30, cmap='viridis')
plt.colorbar(label='f(x,y)')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Ackley Function Landscape')
plt.show()

import random

def random_search(func,bounds, iterations = 1000):
  best_point = None
  best_score = float('inf')

  for _ in range(iterations):
    x = random.uniform(bounds[0], bounds[1])
    y = random.uniform(bounds[0], bounds[1])
    score = func(x, y)
    if score < best_score:
      best_score = score
      best_point = (x, y)

  return best_point, best_score

best_point, best_score = random_search(sphere, (-5, 5))
print('Sphere -> Best_point:', best_point, 'Best_score:', best_score)

best_point, best_score = random_search(rastrigin, (-5.12, 5.12))
print('Rastrigin -> Best_point:', best_point, 'Best_score:', best_score)
best_point, best_score = random_search(ackley, (-5, 5))
print('Ackley -> Best_point:', best_point, 'Best_score:', best_score)
best_point, best_score = random_search(ackley, (-32.768, 32.768))
print('Ackley -> Best_point:', best_point, 'Best_score:', best_score)

"""**Part D**

1. **Which function did Random Search solve best? Why?**

Sphere was solved best because it found score at (0, 0) and the function has a smooth, simple bowl shaped plot. There were no many local minima to confuse random search.

2. **Which function did Random Search struggle with the most?**

Rastrigin was the most difficult because it found the best score at (1,1). Random search did not move intelligently to the desired region, because it has many pockets so it can find local minima without finding global one.

3. **What if iterations increase from 1,000 to 10,000?**

More iterations would generally improve it because of randomly selected points has a higher chance of sampling close to global minimum

4. **What is the main weakness of Random Search?**

It searches blindly, randomly choose points and not learning from previous results leads to bad evaluation missing global minima, stuck to good but non optimal point and need more iterations for difficult landscape.
"""