import datetime
from typing import Optional
from wise_cache.core.formats import convert_timestamp_to_datetime


class TimestampMixin:
    def __init__(self, created: Optional[int] = None, updated: Optional[int] = None):
        self._created = convert_timestamp_to_datetime(created)
        self._updated = convert_timestamp_to_datetime(updated)

    @property
    def created(self) -> Optional[datetime.datetime]:
        """The timestamp indicating the moment when the object was created. Stored as a datetime object. Read-only."""
        return self._created

    @property
    def updated(self) -> Optional[datetime.datetime]:
        """The timestamp indicating the last update of the object. Stored as a datetime object. Read-only."""
        return self._updated

