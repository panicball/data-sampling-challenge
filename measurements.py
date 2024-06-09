from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum

class MeasType(Enum):
    SPO2 = 1
    HR = 2
    TEMP = 3

@dataclass
class Measurement:
    measurementTime: datetime
    measurementType: MeasType
    value: float

def measurement_data_formating(string_from_file: str) -> Measurement:
    # removing curly braces, commas and spaces - basically forming a list of strings
    parts = string_from_file.strip('{}').split(', ')

    # appying correct data types to the list elements
    timestamp = datetime.fromisoformat(parts[0])
    meas_type = MeasType[parts[1]]
    value = float(parts[2])

    return Measurement(timestamp, meas_type, value)
