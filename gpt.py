import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button


# Function to compute the Mandelbrot set
def mandelbrot(xmin, xmax, ymin, ymax, width, height, max_iter):
    x = np.linspace(xmin, xmax, width)
    y = np.linspace(ymin, ymax, height)
    X, Y = np.meshgrid(x, y)
    C = X + 1j * Y
    Z = np.zeros_like(C)
    div_time = np.zeros(Z.shape, dtype=int)
    mask = np.ones(Z.shape, dtype=bool)

    for i in range(max_iter):
        Z[mask] = Z[mask] ** 2 + C[mask]
        mask_new = np.abs(Z) <= 2
        div_now = mask & ~mask_new
        div_time[div_now] = i
        mask = mask_new
    div_time[div_time == 0] = max_iter
    return div_time


# Initial parameters for the fractal
xmin, xmax = -2.0, 1.0
ymin, ymax = -1.5, 1.5
width, height = 800, 800
initial_iter = 50

# Generate the initial Mandelbrot set
mandel = mandelbrot(xmin, xmax, ymin, ymax, width, height, initial_iter)

# Set up the figure and axis
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.3)
im = ax.imshow(mandel, extent=[xmin, xmax, ymin, ymax], cmap='hot', origin='lower')
ax.set_title("Mandelbrot Set")
ax.set_xlabel("Real Axis")
ax.set_ylabel("Imaginary Axis")

# Create a slider to adjust the maximum iterations
ax_iter = plt.axes([0.2, 0.15, 0.65, 0.03])
slider_iter = Slider(ax_iter, 'Iterations', 10, 200, valinit=initial_iter, valstep=1)


# Update function to refresh the plot when slider value changes
def update(val):
    iter_val = int(slider_iter.val)
    mandel_new = mandelbrot(xmin, xmax, ymin, ymax, width, height, iter_val)
    im.set_data(mandel_new)
    im.set_clim(vmin=mandel_new.min(), vmax=mandel_new.max())
    fig.canvas.draw_idle()


slider_iter.on_changed(update)

# Create a reset button to restore the initial iteration count
ax_button = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(ax_button, 'Reset')


def reset(event):
    slider_iter.reset()


button.on_clicked(reset)

plt.show()