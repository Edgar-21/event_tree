from event_tree import NodeBasedTree
import matplotlib.pyplot as plt

top_events = "Ti/DC/BO/U/B-/B2/X/SF/V1/RV/OE/NC/LM/B4/V2/OL/RB"

sequences = {
    "BO": [7.6e-4],
    "BO/U": [7.6e-4, 4.3e-3],
    "BO/U/B-/X/V1/RV/OE/RB": [
        7.6e-4,
        4.3e-3,
        4.9e-1,
        1e-3,
        1,
        5e-1,
        2.75e-1,
        2e-1,
        1 - 4.1e-1,
    ],
    "RV/OE/RB": [0.9, 0.8, 0.7],
}

initiating_frequency = 8e-2
tree = NodeBasedTree(initiating_frequency, top_events)
for sequence, split_fractions in sequences.items():
    tree.add_sequence(sequence, split_fractions)

fig = tree.plot_tree(y_step=-0.5, x_step=1)
plt.axis("off")
plt.savefig("sbo_event_tree.png", bbox_inches="tight")
