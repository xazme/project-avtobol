from datetime import datetime
from pytz import timezone


def generate_article():
    tz = timezone("Africa/Harare")
    date = datetime.now(tz=tz).strftime("%f%d%m%Y%H%M%S")
    article = str(date)
    return article
