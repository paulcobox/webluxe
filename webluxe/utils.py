
from datetime import datetime, timedelta

def get_actual_date():
        today = datetime.today() - timedelta(hours = 5)
        #     date = datetime(today.year, today.month, 1, 0, 0)
        return today