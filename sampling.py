from datetime import datetime, timedelta
from typing import List, Dict
from measurements import Measurement, MeasType

def sampleMeasurements(startOfSampling: datetime, unsampledMeasurements: List[Measurement]) -> Dict[MeasType, List[Measurement]]:
    sampled_data = {MeasType.TEMP: [], MeasType.HR: [], MeasType.SPO2: []}
    measurements_by_type = {MeasType.TEMP: [], MeasType.HR: [], MeasType.SPO2: []}

    for measurement in unsampledMeasurements:
        measurements_by_type[measurement.measurementType].append(measurement)

    for meas_type, measurements in measurements_by_type.items():
        sorted_measurements = sorted(measurements, key=lambda m: m.measurementTime)
        
        interval_start_point = startOfSampling
        last_measurement = None

        for measurement in sorted_measurements:
            
            # if the measurement is older than the current interval
            # add the last measurement (measurement from previous iteration, meaning the last record of previous timestapm) to the sampled data
            # and move to the next time interval
            while measurement.measurementTime >= interval_start_point:
                # if the measurement is exactly at the start of the interval use its value
                if measurement.measurementTime == interval_start_point:
                    last_measurement = measurement
                    break
        
                if last_measurement:
                    last_measurement.measurementTime = interval_start_point
                    sampled_data[meas_type].append(last_measurement)

                interval_start_point += timedelta(minutes=5)
                last_measurement = None

            last_measurement = measurement
        
        if last_measurement:
            last_measurement.measurementTime = interval_start_point
            sampled_data[meas_type].append(last_measurement)

    for meas_type in sampled_data:
        sampled_data[meas_type] = sorted(sampled_data[meas_type], key=lambda m: m.measurementTime)
    
    return sampled_data
