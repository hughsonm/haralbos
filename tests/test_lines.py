import haralbos as hb
import unittest
import math

def linspace(start, stop, step_count):
    samples = [start] + [start + step_index * (stop-start) / step_count for step_index in range(step_count)]
    return samples    

class LineTest(unittest.TestCase):
    def test_round_trip(self):
        test_probabilities = linspace(1e-5, 1.0-1e-5, 1000)
        for prob in test_probabilities:
            round_trip_prob = hb.lines.implied_probability(hb.lines.betting_line(prob))
            self.assertTrue(math.isclose(prob, round_trip_prob))
