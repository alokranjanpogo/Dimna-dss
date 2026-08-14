from utils.volume_lookup import VolumeLookup

# Load volume lookup once
lookup = VolumeLookup()


def get_rule_level(selected_date):
    """
    Jul 1 - Jan 15  : Maintain 524.5 ft
    Jan 16 - Jun 30 : Drawdown allowed till 518 ft
    """

    month = selected_date.month
    day = selected_date.day

    if (
        (month > 1 and month < 7)
        or
        (month == 1 and day >= 16)
    ):
        return 518.0

    return 524.5


def get_rule_volume(selected_date):
    """
    Returns volume corresponding to rule level
    """

    rule_level = get_rule_level(
        selected_date
    )

    return lookup.get_volume(
        rule_level
    )


def get_current_volume(level):
    """
    Returns volume corresponding to entered level
    """

    volume = lookup.get_volume(level)

    if volume is None:
        return 0

    return volume


def get_available_storage(
    level,
    selected_date
):
    """
    Available storage above rule curve
    """

    current_volume = get_current_volume(
        level
    )

    rule_volume = get_rule_volume(
        selected_date
    )

    if (
        current_volume is None
        or
        rule_volume is None
    ):
        return 0

    available_storage = (
        current_volume -
        rule_volume
    )

    return round(
        max(
            available_storage,
            0
        ),
        2
    )


def withdrawal_allowed(
    level,
    selected_date
):
    """
    Checks if withdrawal is allowed
    """

    rule_level = get_rule_level(
        selected_date
    )

    return level > rule_level


def get_buffer_ft(
    level,
    selected_date
):
    """
    How much level is above rule level
    """

    rule_level = get_rule_level(
        selected_date
    )

    return round(
        level - rule_level,
        2
    )


def get_season(selected_date):
    """
    Returns season name
    """

    rule_level = get_rule_level(
        selected_date
    )

    if rule_level == 518:
        return "Drawdown Season"

    return "Storage Season"


def get_status_message(
    level,
    selected_date
):
    """
    Dashboard status message
    """

    if withdrawal_allowed(
        level,
        selected_date
    ):

        return (
            f"Withdrawal Allowed | "
            f"Buffer Available: "
            f"{get_buffer_ft(level, selected_date)} ft"
        )

    return (
        "Withdrawal Not Allowed | "
        "Reservoir below rule level"
    )


def get_dashboard_summary(
    level,
    selected_date
):
    """
    Complete dashboard summary
    """

    return {

        "season":
            get_season(
                selected_date
            ),

        "rule_level":
            get_rule_level(
                selected_date
            ),

        "rule_volume":
            get_rule_volume(
                selected_date
            ),

        "current_volume":
            get_current_volume(
                level
            ),

        "buffer_ft":
            get_buffer_ft(
                level,
                selected_date
            ),

        "available_storage":
            get_available_storage(
                level,
                selected_date
            ),

        "withdrawal_allowed":
            withdrawal_allowed(
                level,
                selected_date
            ),

        "status":
            get_status_message(
                level,
                selected_date
            )
    }
