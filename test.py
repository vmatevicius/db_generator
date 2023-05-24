from datetime import timezone, datetime, timedelta
import random
now = datetime.now()
past_date = now - timedelta(days=1095)
timestamp_now = now.replace(tzinfo=timezone.utc).timestamp()
past_timestamp = past_date.replace(tzinfo=timezone.utc).timestamp()
random_utc = random.uniform(past_timestamp, timestamp_now)
print(timestamp_now)
print(past_timestamp)
print(random_utc)
print(datetime.utcfromtimestamp(random_utc).strftime("%Y-%m-%d"))