from datetime import datetime, timedelta, timezone

def _parse_dt(value: str) -> datetime:
    if not value or not isinstance(value, str):
        raise ValueError("start_time/end_time must be non-empty strings")
    s = value.strip()
    # Support trailing 'Z'
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    # Try ISO first
    try:
        dt = datetime.fromisoformat(s)
    except ValueError as exc:
        raise ValueError(f"Invalid datetime format: {value}") from exc

    # Force timezone-aware (treat naive as UTC)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt

def calculate_duration_and_validate(
    start_time_str: str,
    end_time_str: str,
    *,
    allow_cross_day: bool = True,
    min_minutes: int = 1,
    max_hours: float = 24.0,
) -> tuple[datetime, datetime, float]:
    """
    Parse, normalize to tz-aware datetimes, validate order and bounds.
    Returns (start_dt, end_dt, duration_hours).
    """
    start = _parse_dt(start_time_str)
    end = _parse_dt(end_time_str)

    # Align tz if somehow mismatched objects slip in (defensive)
    if (start.tzinfo is None) ^ (end.tzinfo is None):
        if start.tzinfo is None:
            start = start.replace(tzinfo=end.tzinfo)
        else:
            end = end.replace(tzinfo=start.tzinfo)

    if end < start:
        if allow_cross_day:
            end = end + timedelta(days=1)
        else:
            raise ValueError("end_time must be after start_time")

    duration = end - start
    minutes = duration.total_seconds() / 60.0
    if minutes < min_minutes:
        raise ValueError(f"Duration must be ≥ {min_minutes} minute(s)")

    hours = minutes / 60.0
    if hours > max_hours:
        raise ValueError(f"Duration must be ≤ {max_hours} hours")

    return start, end, round(hours, 2)
