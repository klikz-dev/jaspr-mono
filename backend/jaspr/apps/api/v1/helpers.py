from datetime import datetime, timedelta, tzinfo


class SimpleUTC(tzinfo):
    def tzname(self, **kwargs):
        return "UTC"

    def utcoffset(self, dt: datetime):
        return timedelta(0)


def zulu_time_format(dt: datetime):
    return dt.replace(tzinfo=SimpleUTC()).isoformat()[:-6] + "Z"
