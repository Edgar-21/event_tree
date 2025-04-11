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
    plt.savefig(f"{''.join(title.split())}.svg", format="svg")
    return probabilities


class Node(object):
    def __init__(self, label, parent_node=None, split_fraction=0):
        self.label = label
        self.child_nodes = set({})
        self.parent_node = parent_node
        self.parent_succeeded = False
        self.split_fraction = split_fraction
        self.x = 0
        self.y = 0
        self.vertical_drop = 0

    def determine_child_splits(self):
        terminations = 0
        # print("im a node")
        # print(self.label)
        # print(self.child_nodes)
        for node in self.child_nodes:
            terminations += node.determine_child_splits()
        if not self.child_nodes:
            terminations += 2
        return terminations

    def print_children(self):
        print(self.child_nodes)
        for node in self.child_nodes:
            node.print_children()

    def count_subsequent_failures(self):
        # count how many failures occur if this event succeeds
        failures = 0
        for node in self.child_nodes:
            pass

    def determine_vertical_jog(self, y_step):
        pass

    def set_child_locations(self):
        for child_node in self.child_nodes:
            if child_node.parent_succeeded:
                child_node.x += self.x + self.x_jog
            else:
                child_node.x += self.x + self.x_jog
                child_node.y += self.y + self.y_jog

    def __repr__(self):
        return self.label


class NodeBasedTree(object):

    def __init__(
        self, initiating_frequency, top_events, y_step=-0.5, x_step=1.5
    ):
        self.top_events = top_events.split("/")
        self.initiating_event = self.top_events[0]
        self.parent_node = Node(self.initiating_event)
        self.nodes = {self.initiating_event: self.parent_node}
        self.add_top_sequence()

    def add_top_sequence(self):
        last_node = self.parent_node
        label_str = self.initiating_event + "/"
        self.top_level_nodes = []
        for event in self.top_events[1:]:
            label = event + "|" + label_str.rstrip("/")
            new_node = self.nodes.get(
                label, Node(label, last_node, split_fraction=0)
            )
            new_node.parent_succeeded = True
            self.nodes[label] = new_node
            last_node.child_nodes.add(new_node)
            last_node = new_node
            label_str = label_str + event + "'/"
            self.top_level_nodes.append(new_node)

    def add_sequence(self, sequence, split_fractions):
        events = sequence.split("/")
        events = dict(zip(events, split_fractions))
        last_node = self.parent_node
        label_str = self.initiating_event + "/"
        for top_event in self.top_events[1:]:
            label = top_event + "|" + label_str.rstrip("/")
            active_node = self.nodes.get(
                label, Node(label, last_node, split_fraction=0)
            )
            self.nodes[label] = active_node
            active_node.split_fraction = events.get(top_event, 0)
            if active_node.split_fraction != 0:
                label_str = label_str + top_event + "/"
            else:
                label_str = top_event + "'" + "/" + label_str
                active_node.parent_succeeded = True

            last_node.child_nodes.add(active_node)
            last_node = active_node

    def grow_tree(self):
        # here we want to add in all the implied paths and set the spatial
        # relationships

        # start at the parent node
        self.parent_node.child_nodes[0].set_child_locations()
        pass

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
    top_events = "i/A/B/C"
    sequences = ["A/C", "A/B/C"]
    sequences = {"A": [0.1], "A/C": [0.1, 0.01], "A/B/C": [0.1, 0.2, 0.2]}
    tree = NodeBasedTree(0.08, top_events)
    for sequence, split_fractions in sequences.items():
        tree.add_sequence(sequence, split_fractions)
    # print(tree.parent_node.child_nodes)
    # for label in tree.nodes:
    #     print(tree.nodes[label])
    #     print(tree.nodes[label].child_nodes)
    #     print(tree.nodes[label].split_fraction)
    #     print("loop")
    #     tree.nodes[label].determine_child_splits()
    # print(tree.top_level_nodes)
    node = tree.nodes["C|i/A/B"]
    print(node)
    node.print_children()


if __name__ == "__main__":
    main()
