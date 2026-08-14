from datetime import date

from utils.volume_lookup import (
    VolumeLookup
)

lookup = VolumeLookup()


def get_rule_level(selected_date):

    year = selected_date.year

    jan15 = date(year, 1, 15)

    jun30 = date(year, 6, 30)

    if jan15 < selected_date <= jun30:

        return 518.0

    return 524.5


def get_rule_volume(
    selected_date
):

    rule_level = get_rule_level(
        selected_date
    )

    return lookup.get_volume(
        rule_level
    )


def get_current_volume(
    current_level
):

    volume = lookup.get_volume(
        current_level
    )

    if volume is None:
        return 0

    return volume


def get_available_storage(
    current_level,
    selected_date
):

    current_volume = get_current_volume(
        current_level
    )

    rule_volume = get_rule_volume(
        selected_date
    )

    storage = (
        current_volume -
        rule_volume
    )

    return round(
        max(storage, 0),
        2
    )


def withdrawal_allowed(
    current_level,
    selected_date
):

    return current_level > get_rule_level(
        selected_date
    )


def get_complete_summary(
    current_level,
    selected_date
):

    return {

        "rule_level":
        get_rule_level(
            selected_date
        ),

        "current_volume":
        get_current_volume(
            current_level
        ),

        "rule_volume":
        get_rule_volume(
            selected_date
        ),

        "storage":
        get_available_storage(
            current_level,
            selected_date
        ),

        "withdrawal_allowed":
        withdrawal_allowed(
            current_level,
            selected_date
        )
    }
