from datetime import date

from utils.volume_lookup import VolumeLookup


lookup = VolumeLookup()


def get_rule_level(selected_date):
    """
    Jul 1 - Jan 15  => 524.5 ft
    Jan 16 - Jun 30 => 518 ft
    """

    year = selected_date.year

    jan15 = date(year, 1, 15)
    jun30 = date(year, 6, 30)

    if jan15 < selected_date <= jun30:
        return 518.0

    return 524.5


def get_current_volume(current_level):
    """
    Returns volume corresponding to entered level
    """

    volume = lookup.get_volume(current_level)

    if volume is None:
        return 0

    return volume


def get_target_volume(selected_date):
    """
    Gets target volume from target level
    """

    target_level = get_rule_level(selected_date)

    volume = lookup.get_volume(target_level)

    if volume is None:
        return 0

    return volume


def get_available_storage(current_level, selected_date):
    """
    Available storage above rule curve
    """

    current_volume = get_current_volume(current_level)

    target_volume = get_target_volume(selected_date)

    available_storage = current_volume - target_volume

    if available_storage < 0:
        available_storage = 0

    return round(available_storage, 2)


def withdrawal_allowed(current_level, selected_date):
    """
    Withdrawal permission check
    """

    target_level = get_rule_level(selected_date)

    if current_level > target_level:
        return True

    return False


def get_season(selected_date):

    year = selected_date.year

    jan15 = date(year, 1, 15)
    jun30 = date(year, 6, 30)

    if jan15 < selected_date <= jun30:
        return "Drawdown Season"

    return "Storage Season"


def get_status_message(current_level, selected_date):

    target_level = get_rule_level(selected_date)

    if current_level > target_level:

        surplus = round(
            current_level - target_level,
            2
        )

        return (
            f"Withdrawal Allowed | "
            f"Surplus Level: {surplus} ft"
        )

    return (
        "Withdrawal Not Allowed | "
        "Level Below Rule Curve"
    )


def get_complete_summary(current_level, selected_date):
    """
    Returns everything needed by dashboard
    """

    return {

        "season":
            get_season(selected_date),

        "rule_level":
            get_rule_level(selected_date),

        "current_volume":
            get_current_volume(current_level),

        "rule_volume":
            get_target_volume(selected_date),

        "available_storage":
            get_available_storage(
                current_level,
                selected_date
            ),

        "withdrawal_allowed":
            withdrawal_allowed(
                current_level,
                selected_date
            ),

        "message":
            get_status_message(
                current_level,
                selected_date
            )
    }
