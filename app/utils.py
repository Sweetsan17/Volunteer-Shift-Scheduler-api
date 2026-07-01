from datetime import datetime, timezone
def utc_now():
    """Return the current UTC time (used as a default for created_at columns)."""
    return datetime.now(timezone.utc)
