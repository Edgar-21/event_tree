from event_tree import draw_event_tree

top_events = "Ti/DC/BO/U/B-/B2/X/SF/V1/RV/OE/NC/LM/B4/V2/OL/RB/END STATE"

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
}

initiating_frequency = 8e-2

draw_event_tree(
    initiating_frequency,
    top_events,
    sequences,
    y_step=-0.5,
    x_step=1.5,
    title="SBO Event Tree",
)
