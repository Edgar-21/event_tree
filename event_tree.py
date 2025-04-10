import matplotlib.pyplot as plt
import math
import numpy as np


def draw_event_tree(
    initiating_frequency,
    top_events,
    sequences,
    x_step=2.0,
    y_step=-0.5,
    title="Event Tree",
):
    # Extract events and their failure probabilities from the top_events dictionary
    events = top_events.split("/")
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
        probability = np.prod(sequences[label]) * initiating_frequency
        # Label the end with the event sequence
        ax.text(
            path[-1][0] + 0.2,
            path[-1][1],
            f"{label} {probability:.4e}",
            ha="left",
            va="center",
            fontsize=10,
        )

        # Label each failure event with its probability
        failure_probabilities = sequences[label]
        failure_index = 0
        for i, location in enumerate(path[:-1]):
            # if the y value changes there is a failure
            if not math.isclose(location[1] - path[i + 1][1], 0):
                prob = failure_probabilities[failure_index]
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

    # label top event (all successes)
    ax.text(
        x_coords[-1] + 0.2,
        base_y,
        f"{initiating_frequency-np.sum(list(probabilities.values())):.4e}",
        ha="left",
        va="center",
        fontsize=10,
    )

    # === Final styling ===
    ax.set_xlim(-x_step, x_coords[-1] + x_step)
    ax.set_ylim(min_y - 1, base_y + 1.5)
    ax.axis("off")
    ax.set_title(title, fontsize=14)
    plt.tight_layout()
    plt.savefig(f"{"".join(title.split())}.svg", format="svg")
    return probabilities

class Node(object):
    def __init__(self, label, parent_node=None):
        self.label = label
        self.child_nodes = []
        self.parent_node = parent_node
        self.parent_succeeded = False
        self.split_fraction = None
    
    def add_child_node(self, node):
        if node not in self.child_nodes:
            self.child_nodes.append(node)

    def __repr__(self):
        return self.label

class NodeBasedTree(object):

    def __init__(self, initiating_frequency, top_events, y_step=-0.5, x_step=1.5):
        self.top_events = top_events.split("/")
        self.initiating_event = self.top_events[0]
        self.parent_node = Node(self.initiating_event)
        self.nodes = {self.initiating_event: self.parent_node}
        

    def add_sequence(self, sequence):
        events = sequence.split("/")
        last_node = self.parent_node
        label_str = self.initiating_event+"/"
        for previous_event, event in zip(self.top_events[0:-1], self.top_events[1:]):
            
            if event in events:
                # connect to the last node created
                label = (event+"|"+label_str).rstrip('/')
                new_node = self.nodes.get(label,Node(label, last_node))
                self.nodes[label] = new_node
                last_node = new_node
                label_str += (event+"/")
            

    def plot_event_tree():
        pass

def main():
    # # === Example Usage ===
    # top_events = "Ti/DC/BO/U/END STATE"
    # sequences = {
    #     "DC": [5.3e-5],
    #     "BO": [7.6e-4],
    #     "DC/BO/U": [5.3e-5, 7.6e-4, 4.3e-3],
    #     "DC/BO": [5.3e-5, 7.6e-4],
    # }

    # initiating_frequency = 8e-2

    # _ = draw_event_tree(
    #     initiating_frequency, top_events, sequences, y_step=-0.5, x_step=1.5
    # )
    top_events ="i/A/B/C"
    sequences = ["A/C", "A/B/C"]

    tree = NodeBasedTree(0.08, top_events)
    tree.add_sequence("A/C")

    for label in tree.nodes:
        print(tree.nodes[label].parent_node)

if __name__ == "__main__":
    main()
