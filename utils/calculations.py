from utils.volume_lookup import (
    VolumeLookup
)

lookup = VolumeLookup()


def get_rule_level(selected_date):

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

    rule_level = get_rule_level(
        selected_date
    )

    return lookup.get_volume(
        rule_level
    )


def get_current_volume(level):

    return lookup.get_volume(
        level
    )


def get_available_storage(
    level,
    selected_date
):

    current_volume = get_current_volume(
        level
    )

    rule_volume = get_rule_volume(
        selected_date
    )

    return round(
        current_volume - rule_volume,
        2
    )


def withdrawal_allowed(
    level,
    selected_date
):

    return (
        level >
        get_rule_level(
            selected_date
        )
    )


def get_buffer_ft(
    level,
    selected_date
):

    return round(
        level -
        get_rule_level(
            selected_date
        ),
        2
    )
