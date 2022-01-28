from typing import List
from datetime import datetime


def current_year() -> int:
    now = datetime.now()
    return now.year


def generate_dates() -> List[str]:
    date_ranges: List[str] = []

    # Github started in 2008
    year_range = list(range(2008, current_year() + 1))

    for i, year in enumerate(year_range):
        date_ranges.append(f'{year}-01-01..{year}-12-31')

    return date_ranges
