from datetime import datetime
from pytz import timezone

tz = timezone("Africa/Harare")
date = datetime.now(tz=tz).strftime("%Y%m%d%H%M%S%f")
print(date)
