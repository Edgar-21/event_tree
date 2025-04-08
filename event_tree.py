import matplotlib.pyplot as plt


def draw_event_tree(master_sequence, sequences):
    events = master_sequence.split("/")
    n_events = len(events)

    fig, ax = plt.subplots(figsize=(24, 24))

    y_step = -0.5  # vertical spacing per failure
    base_y = 0  # topmost (success) line y-level

    # Draw master event labels
    for i, event in enumerate(events):
        ax.text(
            i, base_y + 0.4, event, ha="center", fontsize=12, fontweight="bold"
        )

    # === Draw success path ===
    ax.plot(
        range(n_events),
        [base_y] * n_events,
        color="black",
        lw=2,
    )

    # === Draw each failure sequence ===
    for seq_index, sequence in enumerate(sequences):
        failures = sequence.split("/")
        y = base_y  # Start from the top
        x_coords = list(range(n_events))

        # Initialize last_x to track the last position of each branch
        last_x = None

        for i, event in enumerate(events):
            # If this event is in the failure sequence (and not just due to ordering), drop
            if event in failures:
                events_to_the_right = len(events) - i - 1
                new_y = y + y_step * 2 ** (events_to_the_right - 1)
                ax.plot(
                    [i, i], [y, new_y], color="black", lw=2
                )  # vertical drop
                y = new_y

            # Horizontal line to next event
            if i < n_events - 1:
                ax.plot([i, i + 1], [y, y], color="black", lw=2)

            # Track last_x position
            last_x = i

        # Label the end of the branch with the sequence
        ax.text(
            last_x + 0.1,
            y,
            "/".join(failures),
            ha="left",
            va="top",
            fontsize=10,
            color="black",
        )

    # === Style ===
    ax.set_xlim(-0.5, n_events - 0.5 + 1)  # Extend X-axis for jog
    ax.set_ylim(y_step * 2 ** (len(events) - 2))
    ax.axis("off")
    ax.set_title("Event Tree with 'Ti/DC' Branch", fontsize=14)
    plt.tight_layout()
    plt.savefig("out.png")


# === Example Usage ===
master = "Ti/O/DC/BO/U/J/ENDSTATE"
sequences = [
    "U",
    "BO",
    "DC",
    "BO/U",
    "DC/BO/U",
    "DC/BO",
    "DC/U",
    "O",
    "O/DC/BO/U/J",
]
draw_event_tree(master, sequences)
