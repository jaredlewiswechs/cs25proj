import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# Use a nicer built-in style
plt.style.use('ggplot')

# Set random seed for reproducibility
np.random.seed(42)

# Generate synthetic NFL game data for 500 games
n_samples = 500

# Features: passing_yards, rushing_yards, turnovers, penalties
passing_yards = np.random.normal(250, 50, n_samples)  # average passing yards ~250
rushing_yards = np.random.normal(120, 30, n_samples)  # average rushing yards ~120
turnovers = np.random.poisson(1.5, n_samples)  # turnovers (Poisson distribution)
penalties = np.random.poisson(5, n_samples)  # penalty counts (Poisson distribution)

# Define true weights for simulation (influencing win probability):
w_passing = 0.01
w_rushing = 0.02
w_turnovers = -1.5
w_penalties = -0.2
bias = -3.0

# Compute the logistic score for each game
logits = (w_passing * passing_yards +
          w_rushing * rushing_yards +
          w_turnovers * turnovers +
          w_penalties * penalties + bias)

# Calculate win probabilities using the sigmoid function
prob_win = 1 / (1 + np.exp(-logits))

# Generate binary outcomes (win: 1, loss: 0) based on these probabilities
wins = np.random.binomial(1, prob_win)

# Create feature matrix X and target vector y
X = np.column_stack((passing_yards, rushing_yards, turnovers, penalties))
y = wins

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a logistic regression model
clf = LogisticRegression()
clf.fit(X_train, y_train)

# Default values for the sliders
init_passing = 250
init_rushing = 120
init_turnovers = 1.5
init_penalties = 5

# Create the figure with enhanced aesthetics
fig, ax = plt.subplots(figsize=(8, 6))
fig.patch.set_facecolor('#f7f7f7')
ax.set_facecolor('#ffffff')
plt.subplots_adjust(left=0.1, bottom=0.35)

# Create a styled title for the figure
fig.suptitle("NFL Win Probability Predictor", fontsize=22, fontweight='bold', color='#333333')

# Create a text element to display the win probability prediction
pred_text = ax.text(0.5, 0.6, '', fontsize=28, ha='center', va='center',
                    transform=ax.transAxes, color='#007acc')
ax.axis('off')


# Function to update the prediction based on slider values
def update_prediction(val):
    p_yards = slider_passing.val
    r_yards = slider_rushing.val
    t = slider_turnovers.val
    p = slider_penalties.val

    # Create a feature vector from the current slider values
    feature = np.array([[p_yards, r_yards, t, p]])

    # Predict the probability of a win
    pred_prob = clf.predict_proba(feature)[0, 1]

    # Update the text display
    pred_text.set_text(f"Win Probability:\n{pred_prob * 100:.1f}%")
    fig.canvas.draw_idle()


# Create sliders for each feature with a custom background and color
ax_passing = plt.axes([0.1, 0.25, 0.8, 0.03], facecolor='#e0e0e0')
ax_rushing = plt.axes([0.1, 0.20, 0.8, 0.03], facecolor='#e0e0e0')
ax_turnovers = plt.axes([0.1, 0.15, 0.8, 0.03], facecolor='#e0e0e0')
ax_penalties = plt.axes([0.1, 0.10, 0.8, 0.03], facecolor='#e0e0e0')

slider_passing = Slider(ax_passing, 'Passing Yards', 150, 400, valinit=init_passing, valstep=1, color='#007acc')
slider_rushing = Slider(ax_rushing, 'Rushing Yards', 50, 200, valinit=init_rushing, valstep=1, color='#007acc')
slider_turnovers = Slider(ax_turnovers, 'Turnovers', 0, 5, valinit=init_turnovers, valstep=0.1, color='#007acc')
slider_penalties = Slider(ax_penalties, 'Penalties', 0, 15, valinit=init_penalties, valstep=1, color='#007acc')

# Connect slider updates to the prediction update function
slider_passing.on_changed(update_prediction)
slider_rushing.on_changed(update_prediction)
slider_turnovers.on_changed(update_prediction)
slider_penalties.on_changed(update_prediction)

# Create a reset button to restore default slider values
reset_ax = plt.axes([0.8, 0.025, 0.1, 0.04])
button_reset = Button(reset_ax, 'Reset', color='#e0e0e0', hovercolor='#cccccc')


def reset(event):
    slider_passing.reset()
    slider_rushing.reset()
    slider_turnovers.reset()
    slider_penalties.reset()


button_reset.on_clicked(reset)

# Initialize the display with the default prediction
update_prediction(None)

plt.show()