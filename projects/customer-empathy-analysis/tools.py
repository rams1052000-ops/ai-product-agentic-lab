VALID_PRIORITIES = {
    "High": "P1",
    "Medium": "P2",
    "Low": "P3",
}


def calculate_priority(urgency):
    """Convert the model's urgency label into a deterministic business priority."""
    try:
        return VALID_PRIORITIES[urgency]
    except KeyError as exc:
        raise ValueError("Urgency must be High, Medium, or Low.") from exc
