from typing import List, Dict
from measurements import Measurement, MeasType, measurement_data_formating

def read_measurements_from_file(file_name: str) -> List[Measurement]:
    measurements = []
    with open(file_name, 'r') as file:
        for line in file:
            measurements.append(measurement_data_formating(line.strip()))
    return measurements

def write_measurements_to_file(data: Dict[MeasType, List[Measurement]], filename: str):
    with open(filename, 'w') as file:
        for meas_type, measurements in data.items():
            for measurement in measurements:
                file.write(f"{{{measurement.measurementTime.isoformat()}, {meas_type.name}, {measurement.value}}}\n")
