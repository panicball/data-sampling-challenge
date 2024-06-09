import sys
from sampling import sampleMeasurements
from utils import read_measurements_from_file, write_measurements_to_file

def main():
    # checking if the input file is provided as an argument
    if len(sys.argv) != 2:
      raise ValueError("Input file not provided. Programm usage command: python main.py <input_file_name>")
    
    input_file = sys.argv[1]
    measurements = read_measurements_from_file(input_file) 

    # defining the earliest timestamp from the data file
    if measurements:
        earliest_timestamp = min(measurement.measurementTime for measurement in measurements)
    else:
        raise ValueError("No measurements found in the input file.")
    
    # formatting the start of sampling to the nearest 5 minute interval
    # if the minute value is less than 5 - it will be rounded down to 0
    # if the minute value is more than 5 - it will be rounded down to the nearest 5 minute interval
    start_of_sampling = earliest_timestamp.replace(
        minute=(earliest_timestamp.minute // 5) * 5, 
        second=0,
        microsecond=0
    )

    # performing sampling
    sampled_measurements = sampleMeasurements(start_of_sampling, measurements)

    # writing the sampled data to the output file
    write_measurements_to_file(sampled_measurements, "output.txt")
    
    # printing the sampled data to the console, for the sake of easier result checking
    for measurements in sampled_measurements.values():
        for measurement in measurements:
            print(f"{measurement.measurementTime}, {measurement.measurementType.name}, {measurement.value}")

if __name__ == '__main__':
    main()
