import matplotlib.pyplot as plt
import math
import numpy as np


def probability_from_sequence(sequence, probabilities):
    print("hi", sequence)
    failures = sequence.split("/")
    p_vals = []
    for event in probabilities:
        if event in failures:
            p_vals.append(probabilities[event])
    return np.prod(p_vals)


def draw_event_tree(top_events, sequences, x_step=2.0, y_step=-0.5):
    # Extract events and their failure probabilities from the top_events dictionary
    events = list(top_events.keys())
    n_events = len(events)
    base_y = 0  # topmost (success) line y-level

    # === Collect all y positions to determine vertical range ===
    min_y = base_y
    branch_paths = []  # Store branches for final drawing

    for sequence in sequences:
        failures = sequence.split("/")
        y = base_y
        path = [(0, y)]  # Starting point

        for i, event in enumerate(events):
            x = i * x_step
            # Check if the event failed in this sequence
            if event in failures:
                events_to_the_right = len(events) - i - 1
                y += y_step * 2 ** (events_to_the_right - 1)
                path.append((x, y))
                min_y = min(min_y, y)

            if i < n_events - 1:
                next_x = (i + 1) * x_step
                path.append((next_x, y))

        branch_paths.append((path, "/".join(failures)))

    # === Set figure size dynamically based on x/y range ===
    x_range = (n_events - 1) * x_step + x_step
    y_range = abs(min_y - base_y) + 1.5
    fig_width = x_range
    fig_height = y_range
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))

    # === Draw top level event labels ===
    for i, event in enumerate(events):
        x = i * x_step
        if i + 1 != len(events):
            ax.text(
                x,
                base_y + 0.4,
                event,
                ha="center",
                fontsize=12,
                fontweight="bold",
            )
        else:
            ax.text(
                x + 0.2,
                base_y + 0.4,
                event,
                ha="left",
                fontsize=12,
                fontweight="bold",
            )

    # === Draw success path ===
    x_coords = [i * x_step for i in range(n_events)]
    ax.plot(x_coords, [base_y] * n_events, color="black", lw=2)

    probabilities = {}
    # === Draw branches with probabilities ===
    for path, label in branch_paths:
        for j in range(len(path) - 1):
            (x1, y1), (x2, y2) = path[j], path[j + 1]
            ax.plot([x1, x2], [y1, y2], color="black", lw=2)
        probability = probability_from_sequence(label, top_events)
        probability *= list(top_events.values())[0]
        # Label the end with the event sequence
        ax.text(
            path[-1][0] + 0.2,
            path[-1][1],
            f"{label} {probability:.4e}",
            ha="left",
            va="top",
            fontsize=10,
        )

        # Label each failure event with its probability
        failure_probabilities = [top_events[key] for key in label.split("/")]
        failure_index = 0
        print(label)
        print(failure_probabilities)
        for i, location in enumerate(path[:-1]):
            # if the y value changes there is a failure
            if not math.isclose(location[1] - path[i + 1][1], 0):
                prob = failure_probabilities[failure_index]
                print(prob)
                ax.text(
                    path[i + 1][0] + 0.1,
                    path[i + 1][1],
                    f"{prob:.4e}",
                    ha="left",
                    va="bottom",
                    fontsize=8,
                    color="red",
                )
                failure_index += 1
            if failure_index == len(failure_probabilities):
                break
        probabilities[label] = probability

    # === Final styling ===
    ax.set_xlim(-x_step, x_coords[-1] + x_step)
    ax.set_ylim(min_y - 1, base_y + 1.5)
    ax.axis("off")
    ax.set_title("Event Tree with Probabilities", fontsize=14)
    plt.tight_layout()
    plt.savefig("out.svg", format="svg")
    return probabilities


# === Example Usage ===
top_events = {
    "Ti": 8e-2,
    "DC": 5.3e-5,
    "BO": 7.6e-4,
    "U": 4.3e-3,
    "END STATE": 0,
}
sequences = ["DC", "BO", "DC/BO/U", "DC/BO"]
p_dict = draw_event_tree(top_events, sequences, y_step=-0.5, x_step=1)
print(sum(p_dict.values()))
