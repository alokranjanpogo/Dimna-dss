from utils.volume_lookup import VolumeLookup

# Load volume lookup once
lookup = VolumeLookup()


def get_rule_level(selected_date):
    """
    Storage Season :
    Jul 01 to Jan 15 -> 524.5 ft

    Drawdown Season :
    Jan 16 to Jun 30 -> 518.0 ft
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


def get_target_volume(selected_date):
    """
    Returns target volume corresponding
    to the rule level.
    """

    try:

        target_level = get_rule_level(
            selected_date
        )

        return round(
            lookup.get_volume(
                target_level
            ),
            2
        )

    except:

        return 0


def get_current_volume(level):
    """
    Returns current volume from
    volume chart.
    """

    try:

        return round(
            lookup.get_volume(
                level
            ),
            2
        )

    except:

        return 0


def get_available_storage(
    level,
    selected_date
):
    """
    Available storage above target level.
    """

    try:

        current_volume = get_current_volume(
            level
        )

        target_volume = get_target_volume(
            selected_date
        )

        available_storage = (
            current_volume -
            target_volume
        )

        return round(
            max(
                available_storage,
                0
            ),
            2
        )

    except:

        return 0


def get_buffer_ft(
    level,
    selected_date
):
    """
    Buffer above target level.
    """

    try:

        target_level = get_rule_level(
            selected_date
        )

        return round(
            level - target_level,
            2
        )

    except:

        return 0


def withdrawal_allowed(
    level,
    selected_date
):
    """
    Withdrawal allowed if level
    is above target level.
    """

    try:

        target_level = get_rule_level(
            selected_date
        )

        return level > target_level

    except:

        return False


def get_withdrawal_potential(
    level,
    selected_date
):
    """
    Withdrawal potential in MG.
    """

    try:

        return round(
            get_available_storage(
                level,
                selected_date
            ),
            2
        )

    except:

        return 0


def get_season(
    selected_date
):
    """
    Returns season.
    """

    target_level = get_rule_level(
        selected_date
    )

    if target_level == 518.0:

        return "Drawdown Season"

    return "Storage Season"


def get_dashboard_summary(
    level,
    selected_date
):
    """
    Dashboard summary dictionary.
    """

    target_level = get_rule_level(
        selected_date
    )

    current_volume = get_current_volume(
        level
    )

    target_volume = get_target_volume(
        selected_date
    )

    available_storage = get_available_storage(
        level,
        selected_date
    )

    return {

        "season":
            get_season(
                selected_date
            ),

        "current_level":
            level,

        "target_level":
            target_level,

        "current_volume":
            current_volume,

        "target_volume":
            target_volume,

        "available_storage":
            available_storage,

        "withdrawal_potential":
            available_storage,

        "buffer_ft":
            get_buffer_ft(
                level,
                selected_date
            ),

        "withdrawal_allowed":
            withdrawal_allowed(
                level,
                selected_date
            )
    }
