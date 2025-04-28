from event_tree import NodeBasedTree
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

special = 0.482


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


top_events = "Ti/DC/BO/U/B6/BC/X/SF/V1/RV/OE/NC/LM/BD/V2/OL/RB/STBO"

with open("long_term_sbo_events.txt") as f:
    for line in f:
        for event in line.rstrip().split("/"):
            if event not in top_events:
                print(line)


sequences = {
    "BO/B6/BC/X/V1/NC/BD/V2/OL/RB": [
        7.6e-4,
        3.2e-2,
        1.6e-1,
        1,
        1,
        5.4e-1,
        7.7e-1,
        9e-1,
        1,
        0.2,
    ],
    "BO/B6/BC/X/SF/V1/BD/V2/OL/RB": [
        7.6e-4,
        3.2e-2,
        1.6e-1,
        1,
        1,
        1,
        7.7e-1,
        9e-1,
        1,
        0.2,
    ],
    "BO/B6/BC/V1/NC/BD/V2/OL/RB": [
        7.6e-4,
        3.2e-2,
        1.6e-1,
        0.9,
        5.4e-1,
        7.7e-1,
        0.9,
        1,
        0.2,
    ],
    "BO/B6/BC/SF/V1/BD/V2/OL/RB": [
        7.6e-4,
        3.2e-2,
        1.6e-1,
        1,
        0.9,
        7.7e-1,
        0.9,
        1,
        0.2,
    ],
    "BO/B6/X/V1/RV/NC/V2/OL/RB": [
        7.6e-4,
        3.2e-2,
        1e-3,
        1,
        0.5,
        0.36,
        0.01,
        1,
        0.2,
    ],
    "BO/B6/BC/X/V1/NC/V2/OL/RB": [
        7.6e-4,
        3.2e-2,
        0.15,
        1,
        1,
        0.54,
        0.01,
        1,
        0.2,
    ],
    "BO/B6/BC/X/SF/V1/V2/OL/RB": [
        7.6e-4,
        3.2e-2,
        0.15,
        1,
        1,
        0.9,
        0.01,
        1,
        0.2,
    ],
    "BO/B6/V1/RV/NC/V2/OL/RB": [
        7.6e-4,
        3.2e-2,
        0.9,
        0.5,
        0.36,
        0.01,
        1,
        0.2,
    ],
    "BO/B6/BC/V1/NC/V2/OL/RB": [
        7.6e-4,
        3.2e-2,
        0.15,
        0.9,
        0.54,
        0.01,
        1,
        0.2,
    ],
    "BO/B6/BC/SF/V1/V2/OL/RB": [
        7.6e-4,
        3.2e-2,
        0.15,
        1,
        0.9,
        0.01,
        1,
        0.2,
    ],
    "BO/B6/X/V1/RV/NC/LM/RB": [
        7.6e-4,
        3.2e-2,
        1e-3,
        1,
        0.5,
        0.36,
        0.5,
        0.2,
    ],
    "BO/B6/BC/X/V1/NC/BD/RB": [
        7.6e-4,
        3.2e-2,
        0.15,
        1,
        1,
        0.54,
        0.77,
        0.2,
    ],
    "BO/B6/BC/X/V1/NC/LM/RB": [
        7.6e-4,
        3.2e-2,
        0.15,
        1,
        1,
        0.54,
        0.5,
        0.2,
    ],
    "BO/B6/BC/X/SF/V1/BD/RB": [
        7.6e-4,
        3.2e-2,
        1.6e-1,
        1,
        1,
        1,
        7.7e-1,
        0.2,
    ],
    "BO/B6/BC/X/SF/V1/LM/RB": [
        7.6e-4,
        3.2e-2,
        1.6e-1,
        1,
        1,
        1,
        0.5,
        0.2,
    ],
    "BO/B6/BC/X/SF/V1/OE/RB": [
        7.6e-4,
        3.2e-2,
        1.6e-1,
        1,
        1,
        1,
        0.46,
        0.2,
    ],
    "BO/B6/V1/RV/NC/LM/RB": [
        7.6e-4,
        3.2e-2,
        0.9,
        0.5,
        0.36,
        0.5,
        0.2,
    ],
    "BO/B6/BC/V1/NC/BD/RB": [
        7.6e-4,
        3.2e-2,
        0.16,
        0.9,
        0.54,
        0.77,
        0.2,
    ],
    "BO/B6/BC/V1/NC/LM/RB": [
        7.6e-4,
        3.2e-2,
        0.16,
        0.9,
        0.54,
        0.5,
        0.2,
    ],
    "BO/B6/BC/SF/V1/BD/RB": [
        7.6e-4,
        3.2e-2,
        0.16,
        1,
        0.9,
        0.77,
        0.2,
    ],
    "BO/B6/BC/SF/V1/LM/RB": [
        7.6e-4,
        3.2e-2,
        0.16,
        1,
        0.9,
        0.5,
        0.2,
    ],
    "BO/B6/X/RV/NC/LM/RB": [
        7.6e-4,
        3.2e-2,
        0.001,
        0.5,
        0.36,
        0.5,
        0.2,
    ],
    "BO/B6/X/V1/RV/NC/RB": [
        7.6e-4,
        3.2e-2,
        0.001,
        1,
        0.5,
        0.36,
        0.2,
    ],
    "BO/B6/X/V1/RV/OE/RB": [
        7.6e-4,
        3.2e-2,
        0.001,
        1,
        0.5,
        0.46,
        0.2,
    ],
    "BO/B6/BC/X/NC/BD/RB": [
        7.6e-4,
        3.2e-2,
        0.16,
        1,
        0.54,
        0.77,
        0.2,
    ],
    "BO/B6/BC/X/NC/LM/RB": [
        7.6e-4,
        3.2e-2,
        0.16,
        1,
        0.54,
        0.5,
        0.2,
    ],
    "BO/B6/BC/X/V1/NC/RB": [
        7.6e-4,
        3.2e-2,
        0.16,
        1,
        1,
        0.54,
        0.2,
    ],
    "BO/B6/BC/X/V1/OE/RB": [
        7.6e-4,
        3.2e-2,
        0.16,
        1,
        1,
        0.46,
        0.2,
    ],
    "BO/B6/BC/X/SF/BD/RB": [
        7.6e-4,
        3.2e-2,
        0.16,
        1,
        1,
        0.77,
        0.2,
    ],
    "BO/B6/BC/X/SF/LM/RB": [
        7.6e-4,
        3.2e-2,
        0.16,
        1,
        1,
        0.5,
        0.2,
    ],
    "BO/B6/BC/X/SF/V1/RB": [
        7.6e-4,
        3.2e-2,
        0.16,
        1,
        1,
        1,
        0.2,
    ],
    "BO/B6/RV/NC/LM/RB": [
        7.6e-4,
        3.2e-2,
        0.5,
        0.36,
        0.5,
        0.2,
    ],
    "BO/B6/V1/RV/NC/RB": [
        7.6e-4,
        3.2e-2,
        0.9,
        0.5,
        0.36,
        0.2,
    ],
    "BO/B6/BC/NC/BD/RB": [
        7.6e-4,
        3.2e-2,
        0.15,
        0.54,
        0.77,
        0.2,
    ],
    "BO/B6/BC/NC/LM/RB": [
        7.6e-4,
        3.2e-2,
        0.15,
        0.54,
        0.5,
        0.2,
    ],
    "BO/B6/BC/V1/NC/RB": [
        7.6e-4,
        3.2e-2,
        0.15,
        0.9,
        0.54,
        0.2,
    ],
    "BO/B6/BC/SF/BD/RB": [
        7.6e-4,
        3.2e-2,
        0.15,
        1,
        0.77,
        0.2,
    ],
    "BO/B6/BC/SF/LM/RB": [
        7.6e-4,
        3.2e-2,
        0.15,
        1,
        0.5,
        0.2,
    ],
    "BO/B6/BC/SF/V1/RB": [
        7.6e-4,
        3.2e-2,
        0.15,
        1,
        0.9,
        0.2,
    ],
    "BO/B6/X/RV/NC/RB": [
        7.6e-4,
        3.2e-2,
        0.001,
        0.5,
        0.36,
        0.2,
    ],
    "BO/B6/BC/X/NC/RB": [
        7.6e-4,
        3.2e-2,
        0.16,
        1,
        0.54,
        0.2,
    ],
    "BO/B6/BC/X/SF/RB": [
        7.6e-4,
        3.2e-2,
        0.16,
        1,
        1,
        0.2,
    ],
    "BO/B6/RV/NC/RB": [
        7.6e-4,
        3.2e-2,
        0.5,
        0.36,
        0.2,
    ],
    "BO/B6/BC/NC/RB": [
        7.6e-4,
        3.2e-2,
        0.16,
        0.54,
        0.2,
    ],
    "BO/B6/BC/SF/RB": [
        7.6e-4,
        3.2e-2,
        0.16,
        1,
        0.2,
    ],
    "BO/U/STBO": [7.6e-4, 4.3e-3, special],
    "DC/STBO": [5.3e-5, special],
}


initiating_frequency = 8e-2

with open("long_term_sbo_damage.csv", "r") as f:
    damage_states = {}
    for line in f:
        key, value = line.rstrip().split(",")
        damage_states[key] = value


tree = NodeBasedTree(initiating_frequency, top_events)
for sequence, split_fractions in sequences.items():
    tree.add_sequence(sequence, split_fractions)

fig, end_label_list = tree.plot_tree(
    y_step=-0.3, x_step=1, damage_states=damage_states
)
plt.axis("off")
plt.savefig("long_term_sbo_event_tree.png", bbox_inches="tight")
plt.savefig("long_term_sbo_event_tree.pdf", bbox_inches="tight")

with open("long_term_sbo_events.txt", "r") as f:
    end_events = [line.strip() for line in f]

end_label_list = np.array(end_label_list)
missing_events, extra_events = compare_lists(end_label_list[:, 0], end_events)

missing_events.sort(key=len, reverse=True)

print("missing events")
print(len(missing_events))

print("extra events")
print(extra_events)
data_dict = {
    "sequence": end_label_list[:, 0],
    "probability": end_label_list[:, 1],
    "state": end_label_list[:, 2],
}

events = end_label_list[:, 0]
probs = end_label_list[:, 1]
sequence_dict = dict(zip(events, [float(p) for p in probs]))

df = pd.DataFrame(data_dict)
df.to_csv("lt_sbo_summary.csv")

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
print(cd_probability + 1.5550176613342557e-06)
