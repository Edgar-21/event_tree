import matplotlib.pyplot as plt
import math
import numpy as np


def remove_successes(sequence):
    duplicate_sequence = [i for i in sequence]
    for previous_event in sequence:
        if "'" in previous_event:
            duplicate_sequence.remove(previous_event)
    sequence = "/".join(duplicate_sequence)
    return sequence


class Node(object):
    def __init__(self, label, parent_node=None, split_fraction=0):
        self.label = label
        self.child_nodes = set({})
        self.parent_node = parent_node
        self.split_fraction = split_fraction
        self.x = 0
        self.y = 0
        self.y_jog = 0
        self.terminal_node = False

    @property
    def parent_succeeded(self):
        preceeding_sequence = self.label.split("|")[-1]
        parent_event = preceeding_sequence.split("/")[0]
        if "'" in parent_event:
            self._parent_succeeded = True
        else:
            self._parent_succeeded = False
        return self._parent_succeeded

    def print_children(self):
        print(self)
        for node in self.child_nodes:
            node.print_children()

    def count_child_end_states(self):
        # count how many end states connect to this node
        end_states = 0
        for node in self.child_nodes:
            end_states += node.count_child_end_states()
        if len(self.child_nodes) == 0:
            end_states += 1
        if end_states == 0:
            if self.split_fraction != 0:
                end_states = 1
        return end_states

    def determine_vertical_jog(self, y_step):
        end_states = 0

        self.y_jog = y_step

        # if its the end of the line it doesnt matter
        for node in self.child_nodes:
            node.determine_vertical_jog(y_step)
            if node.parent_succeeded:
                end_states = node.count_child_end_states()
                self.y_jog = end_states * y_step

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
        if self.split_fraction != 0:
            if "|" in self.label:
                event, preceeding_sequence = self.label.split("|")
                preceeding_sequence = preceeding_sequence.split("/")
            else:
                event = self.label.split("|")[0]
                preceeding_sequence = ""
            preceeding_sequence = remove_successes(preceeding_sequence)
            ax.annotate(
                f"{self.split_fraction:.2e}",
                (self.x, self.y + self.y_jog),
                textcoords="offset points",
                xytext=(5, 5),
                ha="left",
            )
            ax.annotate(
                event,
                (self.x, self.y + self.y_jog),
                textcoords="offset points",
                xytext=(5, -3),
                ha="left",
                va="top",
            )

    def plot_node_and_children(self, fig):
        self.plot_node(fig)
        for node in self.child_nodes:
            node.plot_node_and_children(fig)

    def connect_with_children(self, fig):
        ax = fig.gca()
        for node in self.child_nodes:
            node.connect_with_children(fig)
            if self.y == node.y:
                ax.plot([self.x, node.x], [self.y, node.y], color="black")
            else:
                ax.plot([self.x, self.x], [self.y, node.y], color="black")
                ax.plot([self.x, node.x], [node.y, node.y], color="black")

    def add_end_states(self, top_events):
        for node in self.child_nodes:
            node.add_end_states(top_events)
        if len(self.child_nodes) == 0 and "|" in self.label:
            event, preceeding_sequence = self.label.split("|")
            last_node = self
            if event != top_events[-1]:
                for next_event in top_events[top_events.index(event) + 1 :]:
                    preceeding_sequence = event + "'/" + preceeding_sequence
                    label = next_event + "|" + preceeding_sequence
                    event = next_event
                    new_node = Node(label, last_node, 0)
                    last_node.child_nodes.add(new_node)
                    last_node = new_node
                pass
            if last_node.split_fraction != 0:
                label = event + "'/" + preceeding_sequence
                success_node = Node(label, last_node)
                label = event + "/" + preceeding_sequence
                failure_node = Node(label, self)
                last_node.child_nodes = set({success_node, failure_node})
            else:
                label = event + "'/" + preceeding_sequence
                success_node = Node(label, last_node)
                last_node.child_nodes = set({success_node})

    def compute_node_probability(self):
        chance_of_occurance = 1
        # ask my parent what their split fraction leading to me was
        if self.parent_node is not None:
            if self.parent_succeeded:
                chance_of_occurance = 1 - self.parent_node.split_fraction
            else:
                chance_of_occurance = self.parent_node.split_fraction
            # parent asks their parent
            chance_of_occurance *= self.parent_node.compute_node_probability()

        return chance_of_occurance

    def label_end_nodes(self, fig, end_label_list, end_states):
        for node in self.child_nodes:
            node.label_end_nodes(fig, end_label_list, end_states)
        if len(self.child_nodes) == 0:
            sequence = self.label.split("/")
            sequence.reverse()
            preceeding_sequence = remove_successes(sequence)
            damage_state = end_states.get(preceeding_sequence, "?")

            probability = self.compute_node_probability()
            ax = fig.gca()
            ax.annotate(
                f"{preceeding_sequence}: {probability:0.2e}, {damage_state}",
                (self.x, self.y - 0.1),
                textcoords="offset points",
                xytext=(5, 5),
                ha="left",
                va="bottom",
            )
            end_label_list.append(
                [preceeding_sequence, probability, damage_state]
            )
        return end_label_list

    def grow_tree(self, top_events):
        for node in self.child_nodes:
            node.grow_tree(top_events)
            node.bud_node(top_events)

    def bud_node(self, top_events):
        if self.split_fraction != 0:
            if len(self.child_nodes) == 1:
                event, preceeding_sequence = self.label.split("|")
                next_event = top_events[top_events.index(event) + 1]
                label = f"{next_event}|{event}'/{preceeding_sequence}"
                new_node = Node(label, self, 0)
                self.child_nodes.add(new_node)

    def __repr__(self):
        return self.label


class NodeBasedTree(object):

    def __init__(self, initiating_frequency, top_events):
        self.top_events = top_events.split("/")
        self.initiating_event = self.top_events[0]
        self.parent_node = Node(
            self.initiating_event, split_fraction=initiating_frequency
        )
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
        last_node = self.parent_node
        label_str = self.initiating_event + "/"

        for top_event in self.top_events[1:]:
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

    def label_top_events(self, fig):
        x_loc = 0
        ax = fig.gca()
        for event in self.top_events:
            ax.annotate(
                f"{event}",
                (x_loc, -self.y_step / 2),
                textcoords="offset points",
                xytext=(5, 5),
                ha="center",
            )
            x_loc += self.x_step

        ax.annotate(
            f"END STATE",
            (x_loc, -self.y_step / 2),
            textcoords="offset points",
            xytext=(5, 5),
            ha="left",
        )

    def plot_tree(self, y_step=-1, x_step=1, damage_states=dict({})):
        self.y_step = y_step
        self.x_step = x_step
        fig = plt.figure()
        self.parent_node.grow_tree(self.top_events)
        self.parent_node.add_end_states(self.top_events)

        self.parent_node.determine_vertical_jog(y_step)
        self.parent_node.set_child_locations(x_step)
        self.parent_node.plot_node_and_children(fig)
        self.parent_node.connect_with_children(fig)
        end_label_list = self.parent_node.label_end_nodes(
            fig, [], end_states=damage_states
        )
        self.label_top_events(fig)

        ax = fig.gca()
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        ax.set_ylim([ylim[0] - 0.5, -y_step + 0.5])
        ylim = ax.get_ylim()

        x_range = xlim[1] - xlim[0]
        y_range = ylim[1] - ylim[0]

        fig.set_size_inches(abs(x_range) + 1, abs(y_range))
        plt.tight_layout()
        return fig, end_label_list


def test_plots(tree, damage_states):
    fig = tree.plot_tree(y_step=-0.3, x_step=1, damage_states=damage_states)

    plt.axis("off")
    plt.tight_layout()
    plt.savefig("test.pdf", bbox_inches="tight")
    # plt.show()

    return tree


def main():
    top_events = "i/A/B/C/D/E"
    sequences = {
        "B/D": [0.1, 0.5],
        "A/B/C/D/E": [0.1, 0.2, 0.3, 0.4, 0.5],
        "E": [0.25],
    }
    damage_states = {
        "i": "ok",
        "i/B/D": "ok",
        "i/A/B/C/D/E": "cd",
        "i/E": "ok",
    }
    tree = NodeBasedTree(0.08, top_events)
    for sequence, split_fractions in sequences.items():
        tree.add_sequence(sequence, split_fractions)
    tree = test_plots(tree, damage_states=damage_states)
    # tree.plot_tree()
    # tree.parent_node.print_children()


if __name__ == "__main__":
    main()
