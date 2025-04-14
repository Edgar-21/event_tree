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
            if self.y == node.y:
                ax.plot([self.x, node.x], [self.y, node.y])
            else:
                ax.plot([self.x, self.x], [self.y, node.y])
                ax.plot([self.x, node.x], [node.y, node.y])
        pass

    def add_end_states(self):
        for node in self.child_nodes:
            node.add_end_states()
        print(self.label)
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
            self.nodes[label] = new_node
            last_node.child_nodes.add(new_node)
            last_node = new_node
            label_str = event + "'/" + label_str
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
                label_str = top_event + "/" + label_str
            else:
                label_str = top_event + "'" + "/" + label_str

            last_node.child_nodes.add(active_node)
            last_node = active_node


def test_plots(tree):
    fig = plt.figure()
    tree.parent_node.add_end_states()
    tree.parent_node.determine_vertical_jog(y_step=-1)
    tree.parent_node.set_child_locations(x_jog=2.5)
    tree.parent_node.plot_node_and_children(fig)

    plt.tight_layout()
    plt.axis("off")
    plt.savefig("nodes.png")

    for node in tree.nodes.values():
        node.connect_with_children(fig)
    plt.axis("off")
    plt.savefig("connect.png")


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
    tn = tree.nodes["C|B'/A'/i"]
    print(tn.child_nodes)
    b = tn.child_nodes[0]
    c = tn.child_nodes[1]
    print(b.parent_succeeded)
    print(c.parent_succeeded)
    print(b.count_child_end_states())


if __name__ == "__main__":
    main()
