from __future__ import annotations

from datetime import datetime
from typing import Any

from .time_utils import format_display_date, format_due_date, format_optional_display_date, utc_isoformat


def _value(item: Any, key: str) -> Any:
    if isinstance(item, dict):
        return item[key]
    return getattr(item, key)


def _optional_value(item: Any, key: str) -> Any:
    if isinstance(item, dict):
        return item.get(key)
    return getattr(item, key, None)


def _kv_lines(items: list[tuple[str, str]]) -> str:
    width = max((len(label) for label, _ in items), default=0)
    return "\n".join(f"{label.ljust(width)}  {value}" for label, value in items)


def format_subject(subject: dict[str, Any]) -> str:
    return _kv_lines(
        [
            ("id", str(_value(subject, "id"))),
            ("display_name", str(_value(subject, "display_name"))),
        ]
    )


def format_subject_list(subjects: list[dict[str, Any]]) -> str:
    if not subjects:
        return "No subjects."
    lines = ["Subjects:"]
    for subject in subjects:
        lines.append(f"- {_value(subject, 'id')}: {_value(subject, 'display_name')}")
    return "\n".join(lines)


def format_location(location: dict[str, Any]) -> str:
    return _kv_lines(
        [
            ("id", str(_value(location, "id"))),
            ("code", str(_value(location, "code"))),
            ("display_name", str(_value(location, "display_name"))),
        ]
    )


def format_location_list(locations: list[dict[str, Any]]) -> str:
    if not locations:
        return "No locations."
    lines = ["Locations:"]
    for location in locations:
        lines.append(f"- {_value(location, 'id')}: {_value(location, 'code')} ({_value(location, 'display_name')})")
    return "\n".join(lines)


def format_episode(episode: dict[str, Any], timezone_name: str = "UTC") -> str:
    items = [
        ("id", str(_value(episode, "id"))),
        ("subject_id", str(_value(episode, "subject_id"))),
        ("location_id", str(_value(episode, "location_id"))),
        ("status", str(_value(episode, "status"))),
        ("current_phase_number", str(_value(episode, "current_phase_number"))),
        ("phase_started_at", format_display_date(_value(episode, "phase_started_at"), timezone_name)),
        ("phase_due_end_at", format_optional_display_date(_optional_value(episode, "phase_due_end_at"), timezone_name)),
        ("healed_at", format_optional_display_date(_optional_value(episode, "healed_at"), timezone_name)),
        ("obsolete_at", format_optional_display_date(_optional_value(episode, "obsolete_at"), timezone_name)),
    ]
    return _kv_lines(items)


def format_episode_list(episodes: list[dict[str, Any]]) -> str:
    if not episodes:
        return "No episodes."
    lines = ["Episodes:"]
    for episode in episodes:
        lines.append(
            f"- {_value(episode, 'id')}: subject {_value(episode, 'subject_id')}, location {_value(episode, 'location_id')}, phase {_value(episode, 'current_phase_number')}, {_value(episode, 'status')}"
        )
    return "\n".join(lines)


def format_application(application: dict[str, Any], timezone_name: str = "UTC") -> str:
    items = [
        ("id", str(_value(application, "id"))),
        ("episode_id", str(_value(application, "episode_id"))),
        ("applied_at", format_display_date(_value(application, "applied_at"), timezone_name)),
        ("treatment_type", str(_value(application, "treatment_type"))),
        ("treatment_name", str(_optional_value(application, "treatment_name"))),
        ("quantity_text", str(_optional_value(application, "quantity_text"))),
        ("phase_number_snapshot", str(_value(application, "phase_number_snapshot"))),
        ("is_voided", str(_value(application, "is_voided"))),
        ("voided_at", format_optional_display_date(_optional_value(application, "voided_at"), timezone_name)),
        ("deleted_at", format_optional_display_date(_optional_value(application, "deleted_at"), timezone_name)),
        ("notes", str(_optional_value(application, "notes"))),
    ]
    return _kv_lines(items)


def format_application_list(applications: list[dict[str, Any]], timezone_name: str = "UTC") -> str:
    if not applications:
        return "No applications."
    lines = ["Applications:"]
    for application in applications:
        lines.append(
            f"- {_value(application, 'id')}: {format_display_date(_value(application, 'applied_at'), timezone_name)} {_value(application, 'treatment_type')} (phase {_value(application, 'phase_number_snapshot')})"
        )
    return "\n".join(lines)


def format_due_list(items: list[dict[str, Any]], timezone_name: str = "UTC") -> str:
    if not items:
        return "No due items."
    lines = ["Due items:"]
    for item in items:
        next_due = format_due_date(_optional_value(item, "next_due_at"), _value(item, "current_phase_number"), timezone_name)
        lines.append(
            f"- episode {_value(item, 'episode_id')}: phase {_value(item, 'current_phase_number')}, due_today={_value(item, 'treatment_due_today')}, next_due={next_due}"
        )
    return "\n".join(lines)


def format_event_list(events: list[dict[str, Any]], timezone_name: str = "UTC") -> str:
    if not events:
        return "No events."
    lines = ["Events:"]
    for event in events:
        lines.append(f"- {_value(event, 'id')}: {format_display_date(_value(event, 'occurred_at'), timezone_name)} {_value(event, 'event_type')} ({_value(event, 'actor_type')})")
    return "\n".join(lines)


def serialize_json_payload(payload: Any) -> Any:
    if isinstance(payload, datetime):
        return utc_isoformat(payload)
    if isinstance(payload, list):
        return [serialize_json_payload(item) for item in payload]
    if isinstance(payload, dict):
        return {key: serialize_json_payload(value) for key, value in payload.items()}
    return payload
