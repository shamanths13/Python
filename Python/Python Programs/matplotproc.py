import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Create a figure and axis
fig, ax = plt.subplots()

# Create a grid of points
x, y = np.linspace(-10, 10, 100), np.linspace(-10, 10, 100)
X, Y = np.meshgrid(x, y)

# Define the vector flow function
def vector_flow(X, Y):
    U = -Y
    V = X
    return U, V

# Plot the initial vector flow
U, V = vector_flow(X, Y)
Q = ax.quiver(X, Y, U, V)

# Create the animation function
def update(num):
    U, V = vector_flow(X, Y)
    Q.set_UVC(U, V)

# Create the animation
ani = FuncAnimation(fig, update, frames=np.arange(0, 2*np.pi, 0.1), repeat=True)

# Show the animation
plt.show()
