#1
from datetime import datetime as dt, timedelta as td

now = dt.now()
prev = now - td(days=5)
print(f"Curr: {now:%Y-%m-%d}")
print(f"Prev: {prev:%Y-%m-%d}")

#2
from datetime import date

today = date.today()
yest  = today - td(days=1)
tmrw  = today + td(days=1)
print(f"Yest: {yest}\nToday: {today}\nTmrw: {tmrw}")

#3
from datetime import datetime as dt

now = dt.now().replace(microsecond=0)
print(f"Clean: {now}")

#4
from datetime import datetime as dt

d1 = dt(2026, 2, 24, 12)
d2 = dt(2026, 2, 20, 10)
diff = d1 - d2
sec = diff.total_seconds()
print(f"Diff: {sec}s")

#5
from datetime import date

birth = date(1900, 5, 17)
today = date.today()
age_days = today - birth
print(f"Born: {birth}")
print(f"Today: {today}")
print(f"You are {age_days.days} days old!")