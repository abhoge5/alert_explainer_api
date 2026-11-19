from models import Alert


NEXT_STEPS = {
    "critical": "Investigate immediately and take corrective action.",
    "warning": "Review the affected system and monitor the metric closely.",
    "info": "Review the metric and confirm whether any action is needed.",
}


def generate_explanation(alert: Alert) -> str:
    """Generate a textual explanation for an alert.

    Args:
        alert: Alert containing the severity, source, title, metric, and threshold
            to describe.

    Returns:
        A sentence describing the alert, its metric compared with the threshold,
        the recommended next step, and its acknowledgement status.

    Raises:
        KeyError: If ``alert.severity`` is not a key in ``NEXT_STEPS``.
    """
    if alert.metric_value > alert.threshold:
        comparison = "exceeded"
    elif alert.metric_value < alert.threshold:
        comparison = "fell below"
    else:
        comparison = "reached"

    next_step = NEXT_STEPS[alert.severity]
    resolved_by = getattr(alert, "resolved_by", None)
    acknowledged_by = resolved_by.upper() if resolved_by else "Not yet acknowledged"
    return (
        f'This {alert.severity} alert from {alert.source} is titled "{alert.title}". '
        f"The {alert.metric_name} metric {comparison} its threshold: the current value is "
        f"{alert.metric_value}, compared with a threshold of {alert.threshold}. "
        f"Recommended next step: {next_step} "
        f"Acknowledged by: {acknowledged_by}."
    )

