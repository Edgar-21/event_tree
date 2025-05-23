from event_tree import NodeBasedTree
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def compare_lists(sub_list, main_list):
    missing_elements = []
    for e in main_list:
        if e not in sub_list:
            missing_elements.append(e)

    extra_elements = []
    for e in sub_list:
        if e not in main_list:
            extra_elements.append(e)
    return missing_elements, extra_elements


top_events = "Ti/DC/BO/U/B-/B2/X/SF/V1/RV/OE/NC/LM/B4/V2/OL/RB"

sequences = {
    "BO/U/B-/B2/X/SF/V1/OE/RB": [
        7.6e-4,
        4.3e-3,
        4.9e-1,
        4.1e-1,
        1e-3,
        1,
        1,
        2.75e-1,
        2e-1,
    ],
    "BO/U/B-/RV/NC/LM/RB": [7.6e-4, 4.3e-3, 4.9e-1, 5e-1, 3.6e-1, 5e-1, 2e-1],
    "BO/U/B-/RV/NC/RB": [7.6e-4, 4.3e-3, 4.9e-1, 5e-1, 3.6e-1, 2e-1],
    "BO/U/B-/V1/RV/NC/LM/RB": [
        7.6e-4,
        4.3e-3,
        4.9e-1,
        1,
        5e-1,
        3.6e-1,
        5e-1,
        2e-1,
    ],
    "BO/U/B-/B2/X/V1/NC/B4/V2/OL/RB": [
        7.6e-4,
        4.3e-3,
        4.9e-1,
        4.1e-1,
        1e-3,
        1,
        5.4e-1,
        3.4e-1,
        9e-1,
        1,
        2e-1,
    ],
    "BO/U/B-/B2/X/SF/V1/B4/V2/OL/RB": [
        7.6e-4,
        4.3e-3,
        4.9e-1,
        4.1e-1,
        1e-3,
        1,
        1,
        3.4e-1,
        9e-1,
        1,
        2e-1,
    ],
    "BO/U/B-/B2/V1/NC/B4/V2/OL/RB": [
        7.6e-4,
        4.3e-3,
        4.9e-1,
        4.1e-1,
        1,
        5.4e-1,
        3.4e-1,
        9e-1,
        1,
        2e-1,
    ],
    "BO/U/B-/B2/SF/V1/B4/V2/OL/RB": [
        7.6e-4,
        4.3e-3,
        4.9e-1,
        4.1e-1,
        1,
        1,
        3.4e-1,
        9e-1,
        1,
        2e-1,
    ],
    "DC/B-/B2/X/V1/NC/B4/V2/OL/RB": [
        5.3e-5,
        4.9e-1,
        4.1e-1,
        1,
        1,
        5.4e-1,
        3.4e-1,
        9e-1,
        1,
        2e-1,
    ],
    "DC/B-/B2/X/SF/V1/B4/V2/OL/RB": [
        5.3e-5,
        4.9e-1,
        4.1e-1,
        1,
        1,
        1,
        3.4e-1,
        9e-1,
        1,
        2e-1,
    ],
    "BO/U/B-/X/V1/RV/NC/V2/OL/RB": [
        7.6e-4,
        4.3e-3,
        4.9e-1,
        1e-3,
        1,
        5e-1,
        3.5e-1,
        1e-2,
        1,
        2e-1,
    ],
    "BO/U/B-/B2/X/V1/NC/V2/OL/RB": [
        7.6e-4,
        4.3e-3,
        4.9e-1,
        4.1e-1,
        1e-3,
        1,
        5.4e-1,
        1e-2,
        1,
        2e-1,
    ],
    "BO/U/B-/B2/X/SF/V1/V2/OL/RB": [
        7.6e-4,
        4.3e-3,
        4.9e-1,
        4.1e-1,
        1e-3,
        1,
        1,
        1e-2,
        1,
        2e-1,
    ],
    "DC/B-/B2/V1/NC/B4/V2/OL/RB": [
        5.3e-5,
        4.9e-1,
        4.1e-1,
        1,
        5.4e-1,
        3.4e-1,
        9e-1,
        1,
        2e-1,
    ],
    "DC/B-/B2/SF/V1/B4/V2/OL/RB": [
        5.3e-5,
        4.9e-1,
        4.1e-1,
        1,
        1,
        3.4e-1,
        9e-1,
        1,
        2e-1,
    ],
    "BO/U/B-/V1/RV/NC/V2/OL/RB": [
        7.6e-4,
        4.3e-3,
        4.9e-1,
        1,
        5e-1,
        3.5e-1,
        1e-2,
        1,
        2e-1,
    ],
    "BO/U/B-/B2/V1/NC/V2/OL/RB": [
        7.6e-4,
        4.3e-3,
        4.9e-1,
        4.1e-1,
        1,
        5.4e-1,
        1e-2,
        1,
        2e-1,
    ],
    "BO/U/B-/B2/SF/V1/V2/OL/RB": [
        7.6e-4,
        4.3e-3,
        4.9e-1,
        4.1e-1,
        1,
        1,
        1e-2,
        1,
        2e-1,
    ],
    "DC/B-/X/V1/RV/NC/V2/OL/RB": [
        5.3e-5,
        4.9e-1,
        1e-5,
        1,
        5e-1,
        3.6e-1,
        1e-2,
        1,
        2e-1,
    ],
    "DC/B-/B2/X/V1/NC/V2/OL/RB": [
        5.3e-5,
        4.9e-1,
        4.1e-1,
        1,
        1,
        5.4e-1,
        1e-2,
        1,
        2e-1,
    ],
    "DC/B-/B2/X/SF/V1/V2/OL/RB": [
        5.3e-5,
        4.9e-1,
        4.1e-1,
        1,
        1,
        1,
        1e-2,
        1,
        2e-1,
    ],
    "BO/U/B-/X/V1/RV/NC/LM/RB": [
        7.6e-4,
        4.3e-3,
        4.9e-1,
        1e-3,
        1,
        5e-1,
        3.5e-1,
        5e-1,
        2e-1,
    ],
    "BO/U/B-/B2/X/V1/NC/B4/RB": [
        7.6e-4,
        4.3e-3,
        4.9e-1,
        4.1e-1,
        1e-3,
        1,
        5.4e-1,
        3.4e-1,
        2e-1,
    ],
    "BO/U/B-/B2/X/V1/NC/LM/RB": [
        7.6e-4,
        4.3e-3,
        4.9e-1,
        4.1e-1,
        1e-3,
        1,
        5.4e-1,
        5e-1,
        2e-1,
    ],
    "BO/U/B-/B2/X/SF/V1/B4/RB": [
        7.6e-4,
        4.3e-3,
        4.9e-1,
        4.1e-1,
        1e-3,
        1,
        1,
        3.4e-1,
        2e-1,
    ],
    "BO/U/B-/B2/X/SF/V1/LM/RB": [
        7.6e-4,
        4.3e-3,
        4.9e-1,
        4.1e-1,
        1e-3,
        1,
        1,
        5e-1,
        2e-1,
    ],
    "BO/U/B-/B2/X/SF/V1/OE/RB": [
        7.6e-4,
        4.3e-3,
        4.9e-1,
        4.1e-1,
        1e-5,
        1,
        1,
        2.75e-1,
        2e-1,
    ],
    "DC/B-/V1/RV/NC/V2/OL/RB": [
        5.3e-5,
        4.9e-1,
        1,
        5e-1,
        3.6e-1,
        1e-2,
        1,
        2e-1,
    ],
    "DC/B-/B2/V1/NC/V2/OL/RB": [
        5.3e-5,
        4.9e-1,
        4.1e-1,
        1,
        5.4e-1,
        1e-2,
        1,
        2e-1,
    ],
    "DC/B-/B2/SF/V1/V2/OL/RB": [5.3e-5, 4.9e-1, 4.1e-1, 1, 1, 1e-2, 1, 2e-1],
    "BO/U/B-/B2/V1/NC/B4/RB": [
        7.6e-4,
        4.3e-3,
        4.9e-1,
        4.1e-1,
        1,
        5.4e-1,
        3.4e-1,
        2e-1,
    ],
    "BO/U/B-/B2/V1/NC/LM/RB": [
        7.6e-4,
        4.3e-3,
        4.9e-1,
        4.1e-1,
        1,
        5.4e-1,
        5e-1,
        2e-1,
    ],
    "BO/U/B-/B2/SF/V1/B4/RB": [
        7.6e-4,
        4.3e-3,
        4.9e-1,
        4.1e-1,
        1,
        1,
        3.4e-1,
        2e-1,
    ],
    "BO/U/B-/B2/SF/V1/LM/RB": [
        7.6e-4,
        4.3e-3,
        4.9e-1,
        4.1e-1,
        1,
        1,
        5e-1,
        2e-1,
    ],
    "DC/B-/X/V1/RV/NC/LM/RB": [
        5.3e-5,
        4.9e-1,
        1e-5,
        1,
        5e-1,
        3.6e-1,
        5e-1,
        2e-1,
    ],
    "DC/B-/B2/X/V1/NC/B4/RB": [
        5.3e-5,
        4.9e-1,
        4.1e-1,
        1,
        1,
        5.4e-1,
        3.4e-1,
        2e-2,
    ],
    "DC/B-/B2/X/V1/NC/LM/RB": [
        5.3e-5,
        4.9e-1,
        4.1e-1,
        1,
        1,
        5.4e-1,
        5e-1,
        2e-2,
    ],
    "DC/B-/B2/X/SF/V1/B4/RB": [5.3e-5, 4.9e-1, 4.1e-1, 1, 1, 1, 3.4e-1, 2e-1],
    "DC/B-/B2/X/SF/V1/LM/RB": [5.3e-5, 4.9e-1, 4.1e-1, 1, 1, 1, 5e-1, 2e-1],
    "DC/B-/B2/X/SF/V1/OE/RB": [5.3e-5, 4.9e-1, 4.1e-1, 1, 1, 1, 2.75e-1, 2e-1],
    "BO/U/B-/X/RV/NC/LM/RB": [
        7.6e-4,
        4.3e-3,
        4.9e-1,
        1e-3,
        5e-1,
        3.6e-1,
        5e-1,
        2e-1,
    ],
    "BO/U/B-/X/V1/RV/NC/RB": [
        7.6e-4,
        4.3e-3,
        4.9e-1,
        1e-3,
        1,
        5e-1,
        3.6e-1,
        2e-1,
    ],
    "BO/U/B-/X/V1/RV/OE/RB": [
        7.6e-4,
        4.3e-3,
        4.9e-1,
        1e-3,
        1,
        5e-1,
        2.75e-1,
        2e-1,
    ],
    "BO/U/B-/B2/X/NC/B4/RB": [
        7.6e-4,
        4.3e-3,
        4.9e-1,
        4.1e-1,
        1e-3,
        5.4e-1,
        3.4e-1,
        2e-1,
    ],
    "BO/U/B-/B2/X/NC/LM/RB": [
        7.6e-4,
        4.3e-3,
        4.9e-1,
        4.1e-1,
        1e-3,
        5.4e-1,
        5e-1,
        2e-1,
    ],
    "BO/U/B-/B2/X/V1/NC/RB": [
        7.6e-4,
        4.3e-3,
        4.9e-1,
        4.1e-1,
        1e-3,
        1,
        5.4e-1,
        2e-1,
    ],
    "BO/U/B-/B2/X/V1/OE/RB": [
        7.6e-4,
        4.3e-3,
        4.9e-1,
        4.1e-1,
        1e-3,
        1,
        2.75e-1,
        2e-1,
    ],
    "BO/U/B-/B2/X/SF/B4/RB": [
        7.6e-4,
        4.3e-3,
        4.9e-1,
        4.1e-1,
        1e-3,
        1,
        3.4e-1,
        2e-1,
    ],
    "BO/U/B-/B2/X/SF/LM/RB": [
        7.6e-4,
        4.3e-3,
        4.9e-1,
        4.1e-1,
        1e-3,
        1,
        5e-1,
        2e-1,
    ],
    "DC/B-/V1/RV/NC/LM/RB": [5.3e-5, 4.9e-1, 1, 5e-1, 3.6e-1, 5e-1, 2e-1],
    "DC/B-/B2/V1/NC/B4/RB": [5.3e-5, 4.9e-1, 4.1e-1, 1, 5.4e-1, 3.4e-1, 2e-1],
    "DC/B-/B2/V1/NC/LM/RB": [5.3e-5, 4.9e-1, 4.1e-1, 1, 5.4e-1, 5e-1, 2e-1],
    "DC/B-/B2/SF/V1/B4/RB": [5.3e-5, 4.9e-1, 4.1e-1, 1, 1, 3.4e-1, 2e-1],
    "DC/B-/B2/SF/V1/LM/RB": [5.3e-5, 4.9e-1, 4.1e-1, 1, 1, 5e-1, 2e-1],
    "BO/U/B-/V1/RV/NC/RB": [7.6e-4, 4.3e-3, 4.9e-1, 1, 5e-1, 3.6e-1, 2e-1],
    "BO/U/B-/B2/NC/B4/RB": [
        7.6e-4,
        4.3e-3,
        4.9e-1,
        4.1e-1,
        5.4e-1,
        3.4e-1,
        2e-1,
    ],
    "BO/U/B-/B2/NC/LM/RB": [
        7.6e-4,
        4.3e-3,
        4.9e-1,
        4.1e-1,
        5.4e-1,
        5e-1,
        2e-1,
    ],
    "BO/U/B-/B2/V1/NC/RB": [7.6e-4, 4.3e-3, 4.9e-1, 4.1e-1, 1, 5.4e-1, 2e-1],
    "BO/U/B-/B2/SF/B4/RB": [7.6e-4, 4.3e-3, 4.9e-1, 4.1e-1, 1, 3.4e-1, 2e-1],
    "BO/U/B-/B2/SF/LM/RB": [7.6e-4, 4.3e-3, 4.9e-1, 4.1e-1, 1, 5e-1, 2e-1],
    "BO/U/B-/B2/SF/V1/RB": [7.6e-4, 4.3e-3, 4.9e-1, 4.1e-1, 1, 1, 2e-1],
    "DC/B-/X/RV/NC/LM/RB": [5.3e-5, 4.9e-1, 1e-3, 5e-1, 3.6e-1, 5e-1, 2e-1],
    "DC/B-/X/V1/RV/NC/RB": [5.3e-5, 4.9e-1, 1e-3, 1, 5e-1, 3.6e-1, 2e-1],
    "DC/B-/X/V1/RV/OE/RB": [5.3e-5, 4.9e-1, 1e-3, 1, 5e-1, 2.75e-1, 2e-1],
    "BO/U/B-/B2/X/SF/V1/RB": [
        7.6e-4,
        4.3e-3,
        4.9e-1,
        4.1e-1,
        1e-3,
        1,
        1,
        2e-1,
    ],
    "DC/B-/B2/X/NC/B4/RB": [5.3e-5, 4.9e-1, 4.1e-1, 1, 5.4e-1, 3.4e-1, 2e-1],
    "DC/B-/B2/X/NC/LM/RB": [5.3e-5, 4.9e-1, 4.1e-1, 1, 5.4e-1, 5e-1, 2e-1],
    "DC/B-/B2/X/V1/NC/RB": [5.3e-5, 4.9e-1, 4.1e-1, 1, 1, 5.4e-1, 2e-1],
    "DC/B-/B2/X/V1/OE/RB": [5.3e-5, 4.9e-1, 4.1e-1, 1, 1, 2.75e-1, 2e-1],
    "DC/B-/B2/X/SF/B4/RB": [5.3e-5, 4.9e-1, 4.1e-1, 1, 1, 3.4e-1, 2e-1],
    "DC/B-/B2/X/SF/LM/RB": [5.3e-5, 4.9e-1, 4.1e-1, 1, 1, 5e-1, 2e-1],
    "DC/B-/B2/X/SF/V1/RB": [5.3e-5, 4.9e-1, 4.1e-1, 1, 1, 1, 2e-1],
    "BO/U/B-/X/RV/NC/RB": [7.6e-4, 4.3e-3, 4.9e-1, 1e-3, 5e-1, 3.6e-1, 2e-1],
    "BO/U/B-/B2/X/NC/RB": [7.6e-4, 4.3e-3, 4.9e-1, 4.1e-1, 1e-3, 5.4e-1, 2e-1],
    "BO/U/B-/B2/X/SF/RB": [7.6e-4, 4.3e-3, 4.9e-1, 4.1e-1, 1e-3, 1, 2e-1],
    "DC/B-/RV/NC/LM/RB": [5.3e-5, 4.9e-1, 5e-1, 3.6e-1, 5e-1, 2e-1],
    "DC/B-/V1/RV/NC/RB": [5.3e-5, 4.9e-1, 1, 5e-1, 3.6e-1, 2e-1],
    "DC/B-/B2/NC/B4/RB": [5.3e-5, 4.9e-1, 4.1e-1, 5.4e1, 3.4e-1, 2e-1],
    "DC/B-/B2/NC/LM/RB": [5.3e-5, 4.9e-1, 4.1e-1, 5.4e1, 5e-1, 2e-1],
    "DC/B-/B2/V1/NC/RB": [5.3e-5, 4.9e-1, 4.1e-1, 1, 5.4e-1, 2e-1],
    "DC/B-/B2/SF/B4/RB": [5.3e-5, 4.9e-1, 4.1e-1, 1, 3.4e-1, 2e-1],
    "DC/B-/B2/SF/LM/RB": [5.3e-5, 4.9e-1, 4.1e-1, 1, 5e-1, 2e-1],
    "DC/B-/B2/SF/V1/RB": [5.3e-5, 4.9e-1, 4.1e-1, 1, 1, 2e-1],
    "BO/U/B-/B2/NC/RB": [7.6e-4, 4.3e-3, 4.9e-1, 4.1e-1, 5.4e-1, 2e-1],
    "BO/U/B-/B2/SF/RB": [7.6e-4, 4.3e-3, 4.9e-1, 4.1e-1, 1, 2e-1],
    "DC/B-/X/RV/NC/RB": [5.3e-5, 4.9e-1, 1e-3, 5e-1, 3.6e-1, 2e-1],
    "DC/B-/B2/X/NC/RB": [5.3e-5, 4.9e-1, 4.1e-1, 1, 5.4e-1, 2e-1],
    "DC/B-/B2/X/SF/RB": [5.3e-5, 4.9e-1, 4.1e-1, 1, 1, 2e-1],
    "DC/B-/RV/NC/RB": [5.3e-5, 4.9e-1, 5e-1, 3.6e-1, 2e-1],
    "DC/B-/B2/NC/RB": [5.3e-5, 4.9e-1, 4.1e-1, 5.4e-1, 2e-1],
    "DC/B-/B2/SF/RB": [5.3e-5, 4.9e-1, 4.1e-1, 1, 2e-1],
}

initiating_frequency = 8e-2
tree = NodeBasedTree(initiating_frequency, top_events)
for sequence, split_fractions in sequences.items():
    tree.add_sequence(sequence, split_fractions)

with open("short_term_sbo_damage.csv", "r") as f:
    damage_states = {}
    for line in f:
        key, value = line.rstrip().split(",")
        damage_states[key] = value

fig, end_label_list = tree.plot_tree(
    y_step=-0.3, x_step=1, damage_states=damage_states
)
plt.axis("off")
plt.savefig("short_term_sbo_event_tree.png", bbox_inches="tight")
plt.savefig("short_term_sbo_event_tree.pdf", bbox_inches="tight")

with open("short_term_sbo_events.txt", "r") as f:
    end_events = [line.strip() for line in f]
end_label_list = np.array(end_label_list)
missing_events, extra_events = compare_lists(end_label_list[:, 0], end_events)

missing_events.sort(key=len, reverse=True)


events = end_label_list[:, 0]
probs = end_label_list[:, 1]

sequence_dict = dict(zip(events, [float(p) for p in probs]))


cd_probability = 0
ok_probability = 0
for sequence, probability in sequence_dict.items():
    if damage_states[sequence] == "n":
        cd_probability += probability
    if damage_states[sequence] == "ok":
        ok_probability += probability

print(cd_probability)
print(ok_probability)
print(cd_probability + ok_probability)

print(end_label_list.shape)

data_dict = {
    "sequence": end_label_list[:, 0],
    "probability": end_label_list[:, 1],
    "state": end_label_list[:, 2],
}

df = pd.DataFrame(data_dict)
df.to_csv("st_sbo_summary.csv")
