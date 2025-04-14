import matplotlib.pyplot as plt
import math
import numpy as np


class Node(object):
    def __init__(self, label, parent_node=None, split_fraction=0):
        self.label = label
        self.child_nodes = set({})
        self.parent_node = parent_node
        self.split_fraction = split_fraction
        self.x = 0
        self.y = 0
        self.y_jog = 0

    @property
    def parent_succeeded(self):
        preceeding_sequence = self.label.split("|")[-1]
        parent_event = preceeding_sequence.split("/")[0]
        if "'" in parent_event:
            self._parent_succeeded = True
        else:
            self._parent_succeeded = False
        return self._parent_succeeded

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
        for node in self.child_nodes:
            node.print_children()

    def count_child_end_states(self):
        # count how many end states connect to this node
        end_states = 0
        for node in self.child_nodes:
            end_states += node.count_child_end_states()
        if len(self.child_nodes) == 0:
            end_states += 1
        return end_states

    def determine_vertical_jog(self, y_step):
        end_states = 0

        # if its the end of the line it doesnt matter
        for node in self.child_nodes:
            node.determine_vertical_jog(y_step)
            if node.parent_succeeded:
                end_states = node.count_child_end_states()

        self.y_jog = (end_states) * y_step

    def set_child_locations(self, x_jog):
        for child_node in self.child_nodes:
            if child_node.parent_succeeded:
                child_node.x += self.x + x_jog
                child_node.y = self.y
            else:
                child_node.x += self.x + x_jog
                child_node.y += self.y + self.y_jog
            child_node.set_child_locations(x_jog=x_jog)

    def plot_node(self, fig):
        ax = fig.gca()  # Get the current axes from the figure
        ax.plot(self.x, self.y, "o")  # Plot the point using the axes
        ax.annotate(
            f"P({self.label})={self.split_fraction:.4e}",
            (self.x, self.y + self.y_jog),
            textcoords="offset points",
            xytext=(5, 5),
            ha="left",
        )  # Add label next to the point

    def plot_node_and_children(self, fig):
        self.plot_node(fig)
        for node in self.child_nodes:
            node.plot_node_and_children(fig)

    def connect_with_children(self, fig):
        ax = fig.gca()
        for node in self.child_nodes:
            node.connect_with_children(fig)
            if self.y == node.y:
                ax.plot([self.x, node.x], [self.y, node.y])
            else:
                ax.plot([self.x, self.x], [self.y, node.y])
                ax.plot([self.x, node.x], [node.y, node.y])
        pass

    def add_end_states(self):
        for node in self.child_nodes:
            node.add_end_states()
        if "|" in self.label:
            event, preceeding_sequence = self.label.split("|")
        if len(self.child_nodes) == 0:
            if self.split_fraction != 0:
                label = event + "'/" + preceeding_sequence
                success_node = Node(label, self)
                label = event + "/" + preceeding_sequence
                failure_node = Node(label, self)
                self.child_nodes = [success_node, failure_node]
            else:
                label = event + "'/" + preceeding_sequence
                success_node = Node(label, self)
                self.child_nodes = [success_node]

    def __repr__(self):
        return self.label


class NodeBasedTree(object):

    def __init__(self, initiating_frequency, top_events):
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
            self.nodes[label] = new_node
            last_node.child_nodes.add(new_node)
            last_node = new_node
            label_str = event + "'/" + label_str
            self.top_level_nodes.append(new_node)

    def add_sequence(self, sequence, split_fractions):

        events_list = sequence.split("/")
        events = dict(zip(events_list, split_fractions))
        print(sequence)
        print(events)
        last_node = self.parent_node
        label_str = self.initiating_event + "/"

        for top_event in self.top_events[1:]:
            print(top_event)
            label = top_event + "|" + label_str.rstrip("/")
            active_node = self.nodes.get(
                label, Node(label, last_node, split_fraction=0)
            )
            self.nodes[label] = active_node
            active_node.split_fraction = max(
                events.get(top_event, 0), active_node.split_fraction
            )

            if top_event in events:
                label_str = top_event + "/" + label_str
            else:
                label_str = top_event + "'" + "/" + label_str

            last_node.child_nodes.add(active_node)
            last_node = active_node

    def plot_tree(self, y_step=-1, x_step=1):
        fig = plt.figure()
        self.parent_node.add_end_states()
        self.parent_node.determine_vertical_jog(y_step)
        self.parent_node.set_child_locations(x_step)
        self.parent_node.plot_node_and_children(fig)
        self.parent_node.connect_with_children(fig)

        ax = fig.gca()
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()

        x_range = xlim[1] - xlim[0]
        y_range = ylim[1] - ylim[0]

        fig.set_size_inches(abs(x_range), abs(y_range))

        return fig


def test_plots(tree):
    fig = tree.plot_tree(y_step=-1, x_step=4)

    plt.tight_layout()
    plt.axis("off")
    plt.savefig("connect.png", bbox_inches="tight")


def main():
    top_events = "i/A/B/C"
    sequences = {
        "A": [0.1],
        "B/C": [0.1, 0.01],
        "A/B/C": [0.1, 0.2, 0.2],
        "C": [0.5],
    }
    tree = NodeBasedTree(0.08, top_events)
    for sequence, split_fractions in sequences.items():
        tree.add_sequence(sequence, split_fractions)
    test_plots(tree)

    tn = tree.nodes["B|A'/i"]
    print(tn.split_fraction)
    print(tn.parent_node)


if __name__ == "__main__":
    main()
