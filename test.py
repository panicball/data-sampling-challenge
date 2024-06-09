import unittest
from datetime import datetime
from measurements import Measurement, MeasType
from sampling import sampleMeasurements

class TestSampling(unittest.TestCase):

    def setUp(self):
        self.start_time = datetime(2017, 1, 3, 10, 0, 0)

        self.measurements = [
            Measurement(datetime(2017, 1, 3, 10, 4, 45), MeasType.TEMP, 35.79),
            Measurement(datetime(2017, 1, 3, 10, 1, 18), MeasType.SPO2, 98.78),
            Measurement(datetime(2017, 1, 3, 10, 9, 7), MeasType.TEMP, 35.01),
            Measurement(datetime(2017, 1, 3, 10, 3, 34), MeasType.SPO2, 96.49),
            Measurement(datetime(2017, 1, 3, 10, 2, 1), MeasType.TEMP, 35.82),
            Measurement(datetime(2017, 1, 3, 10, 5, 0), MeasType.SPO2, 97.17),
            Measurement(datetime(2017, 1, 3, 10, 5, 1), MeasType.SPO2, 95.08),
        ]

    def test_challenge_example_measurements(self):
        sampled = sampleMeasurements(self.start_time, self.measurements)
        
        self.assertEqual(len(sampled[MeasType.TEMP]), 2)
        self.assertEqual(sampled[MeasType.TEMP][0].value, 35.79)
        self.assertEqual(sampled[MeasType.TEMP][1].value, 35.01)

        self.assertEqual(len(sampled[MeasType.SPO2]), 2)
        self.assertEqual(sampled[MeasType.SPO2][0].value, 97.17)
        self.assertEqual(sampled[MeasType.SPO2][1].value, 95.08)

    def test_empty_input_data(self):
        sampled = sampleMeasurements(self.start_time, [])
        self.assertEqual(sampled, {MeasType.TEMP: [], MeasType.HR: [], MeasType.SPO2: []})

    def test_single_measurement(self):
        single_measurement = [Measurement(datetime(2017, 1, 3, 10, 2, 0), MeasType.TEMP, 36.0)]
        sampled = sampleMeasurements(self.start_time, single_measurement)
        self.assertEqual(len(sampled[MeasType.TEMP]), 1)
        self.assertEqual(sampled[MeasType.TEMP][0].value, 36.0)

    def test_multiple_measurements_in_the_same_interval(self):
        measurements = [
            Measurement(datetime(2017, 1, 3, 10, 1, 0), MeasType.TEMP, 36.0),
            Measurement(datetime(2017, 1, 3, 10, 3, 0), MeasType.TEMP, 37.0),
            Measurement(datetime(2017, 1, 3, 10, 4, 0), MeasType.TEMP, 38.0),
        ]
        sampled = sampleMeasurements(self.start_time, measurements)
        self.assertEqual(len(sampled[MeasType.TEMP]), 1)
        self.assertEqual(sampled[MeasType.TEMP][0].value, 38.0)

    def test_measurements_that_match_interval_border(self):
        measurements = [
            Measurement(datetime(2017, 1, 3, 10, 0, 0), MeasType.TEMP, 36.0),
            Measurement(datetime(2017, 1, 3, 10, 0, 1), MeasType.TEMP, 36.1),
            Measurement(datetime(2017, 1, 3, 10, 5, 0), MeasType.TEMP, 37.0),
            Measurement(datetime(2017, 1, 3, 10, 5, 1), MeasType.TEMP, 37.1),
            Measurement(datetime(2017, 1, 3, 10, 10, 0), MeasType.TEMP, 38.0),
            Measurement(datetime(2017, 1, 3, 10, 10, 1), MeasType.TEMP, 38.1),
        ]
        sampled = sampleMeasurements(self.start_time, measurements)

        self.assertEqual(len(sampled[MeasType.TEMP]), 4)
        self.assertEqual(sampled[MeasType.TEMP][0].value, 36.0)
        self.assertEqual(sampled[MeasType.TEMP][1].value, 37.0)
        self.assertEqual(sampled[MeasType.TEMP][2].value, 38.0)
        self.assertEqual(sampled[MeasType.TEMP][3].value, 38.1)

    def test_overlapping_time_intervals(self):
        measurements = [
            Measurement(datetime(2017, 1, 3, 10, 4, 59), MeasType.TEMP, 36.0),
            Measurement(datetime(2017, 1, 3, 10, 5, 0), MeasType.TEMP, 37.0),
            Measurement(datetime(2017, 1, 3, 10, 5, 1), MeasType.TEMP, 38.0)
        ]
        sampled = sampleMeasurements(self.start_time, measurements)
        expected = {MeasType.SPO2: [], MeasType.HR: [], MeasType.TEMP: [
            Measurement(datetime(2017, 1, 3, 10, 5, 0), MeasType.TEMP, 37.0),
            Measurement(datetime(2017, 1, 3, 10, 10, 0), MeasType.TEMP, 38.0)
        ]}
        self.assertEqual(sampled, expected)

    def test_measurements_within_same_time_moment(self):
        same_second_measurements = [
            Measurement(datetime(2017, 1, 3, 10, 1, 0), MeasType.TEMP, 36.5),
            Measurement(datetime(2017, 1, 3, 10, 1, 0), MeasType.TEMP, 36.6)
        ]
        result = sampleMeasurements(self.start_time, same_second_measurements)
        self.assertEqual(len(result[MeasType.TEMP]), 1)
        self.assertEqual(result[MeasType.TEMP][0].value, 36.6)

if __name__ == '__main__':
    unittest.main()
