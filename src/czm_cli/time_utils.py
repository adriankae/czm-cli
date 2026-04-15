from __future__ import annotations

from datetime import date, datetime, time, timezone
from zoneinfo import ZoneInfo


def get_zone(timezone_name: str) -> ZoneInfo:
    return ZoneInfo(timezone_name)


def parse_local_datetime(value: str, timezone_name: str) -> datetime:
    normalized = value.strip()
    candidate = normalized.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(candidate)
    except ValueError:
        parsed_date = date.fromisoformat(normalized)
        parsed = datetime.combine(parsed_date, time.min)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=get_zone(timezone_name))
    return parsed.astimezone(timezone.utc)


def utc_isoformat(dt: datetime) -> str:
    aware = dt.astimezone(timezone.utc)
    return aware.isoformat().replace("+00:00", "Z")

