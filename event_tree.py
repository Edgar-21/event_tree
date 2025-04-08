import matplotlib.pyplot as plt


def draw_event_tree(master_sequence, sequences):
    events = master_sequence.split("/")
    n_events = len(events)

    fig, ax = plt.subplots(figsize=(12, 5))

    y_step = -1.5  # vertical spacing per failure
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
        color="green",
        lw=2,
        label="Success Path",
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
                new_y = y + y_step
                ax.plot([i, i], [y, new_y], color="red", lw=2)  # vertical drop
                y = new_y

            # Horizontal line to next event
            if i < n_events - 1:
                ax.plot([i, i + 1], [y, y], color="red", lw=2)

            # Track last_x position
            last_x = i

        # Label the end of the branch with the sequence
        ax.text(
            last_x + 0.1,
            y - 0.3,
            "/".join(failures),
            ha="left",
            va="top",
            fontsize=10,
            color="red",
        )

    # === Style ===
    ax.set_xlim(-0.5, n_events - 0.5 + 1)  # Extend X-axis for jog
    ax.set_ylim(y_step * (len(sequences) + 1), base_y + 1.5)
    ax.axis("off")
    ax.set_title("Event Tree with 'Ti/DC' Branch", fontsize=14)
    ax.legend()
    plt.tight_layout()
    plt.show()


# === Example Usage ===
master = "Ti/DC/BO/U/ENDSTATE"
sequences = ["DC", "DC/BO", "DC/U"]
draw_event_tree(master, sequences)
