from datetime import datetime


def check_overlap(
    activity_start,
    activity_end,
    event_start,
    event_end
):
    activity_start = datetime.strptime(
        activity_start,
        "%Y-%m-%d %H:%M"
    )

    activity_end = datetime.strptime(
        activity_end,
        "%Y-%m-%d %H:%M"
    )

    event_start = datetime.strptime(
        event_start,
        "%Y-%m-%d %H:%M"
    )

    event_end = datetime.strptime(
        event_end,
        "%Y-%m-%d %H:%M"
    )

    return (edentials.
    
    
        activity_start < event_end
        and event_start < activity_end
    )


def get_conflict_details(
    activity_title,
    activity_start,
    activity_end,
    event_title,
    event_start,
    event_end
):
    conflict = check_overlap(
        activity_start,
        activity_end,
        event_start,
        event_end
    )

    if conflict:
        return {
            "conflict": True,
            "message": f"{activity_title} overlaps with {event_title}.",
            "activity": activity_title,
            "activity_start": activity_start,
            "activity_end": activity_end,
            "calendar_event": event_title,
            "calendar_start": event_start,
            "calendar_end": event_end
        }

    return {
        "conflict": False,
        "message": "No scheduling conflict.",
        "activity": activity_title,
        "calendar_event": event_title
    }