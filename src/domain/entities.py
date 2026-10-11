from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass(frozen=True)
class Observation:
    series_id: str
    date: date
    value: Decimal