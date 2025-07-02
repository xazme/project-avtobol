import random
from datetime import datetime
from pytz import timezone


def generate_article():
    tz = timezone("Africa/Harare")
    now = datetime.now(tz=tz)
    timestamp_ms = int(now.timestamp()) * random.randint(1000, 9999)
    return str(timestamp_ms)
