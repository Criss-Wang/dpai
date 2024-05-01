import contextvars
from datetime import datetime as dt

launch_date = contextvars.ContextVar("launch_date", default=dt.utcnow())
