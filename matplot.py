import matplotlib.pyplot as plt
import random
from matplotlib.widgets import Button, Slider

# Parameters for the data
n_points = 100
min_sleep = 4
max_sleep = 10
noise_range = 5
correlation_factor = 4

# Function to generate data based on current noise level
def generate_data(n_points, noise_range):
    hours_sleep = [round(random.uniform(min_sleep, max_sleep), 1) for _ in range(n_points)]
    grade = [round(60 + (sleep * correlation_factor) + random.uniform(-noise_range, noise_range), 1) for sleep in hours_sleep]
    return hours_sleep, grade

# Generate initial data
hours_sleep, grade = generate_data(n_points, noise_range)

# Create the figure and adjust the layout to make room for interactive widgets
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.3)

# Plot the initial scatter plot
sc = ax.scatter(hours_sleep, grade)
ax.set_title("Sleep vs. Grades")
ax.set_xlabel("Hours of Sleep")
ax.set_ylabel("Grade (%)")
ax.grid(True)

# Create a button for regenerating the data
ax_button = plt.axes([0.1, 0.15, 0.2, 0.075])
button = Button(ax_button, 'Regenerate')

# Create a slider to adjust the noise level
ax_slider = plt.axes([0.4, 0.15, 0.4, 0.03])
noise_slider = Slider(ax_slider, 'Noise', 0, 10, valinit=noise_range, valstep=0.1)

# Define the update function to regenerate and update the plot
def update_data(event):
    # Get the current noise level from the slider
    current_noise = noise_slider.val
    # Generate new data with the updated noise level
    new_hours_sleep, new_grade = generate_data(n_points, current_noise)

    # Clear the current axes and redraw the scatter plot
    ax.cla()
    ax.scatter(new_hours_sleep, new_grade)
    ax.set_title("Sleep vs. Grades")
    ax.set_xlabel("Hours of Sleep")
    ax.set_ylabel("Grade (%)")
    ax.grid(True)

    # Redraw the canvas
    fig.canvas.draw_idle()

# Connect the update function to the button and slider
button.on_clicked(update_data)
noise_slider.on_changed(update_data)

plt.show()