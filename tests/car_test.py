import unittest
import time
from smartpark.car import Car

class TestCar(unittest.TestCase):
    """car should start with no entry or exit time"""
    def test_initial_state(self):
        c = Car("ABC123")
        self.assertEqual(c.license_plate, "ABC123")
        self.assertIsNone(c.entry_time)
        self.assertIsNone(c.exit_time)

    def test_record_entry(self):
        """record_entry() should set entry_time"""
        c = Car("XYZ789")
        c.record_entry()
        self.assertIsNotNone(c.entry_time)
        self.assertAlmostEqual(c.entry_time, time.time(), delta=0.01)

    def test_record_exit(self):
        """record_exit() should set exit_time"""
        c = Car("XYZ789")
        c.record_entry()
        time.sleep(0.01) # small delay so exit_time is different
        c.record_exit()
        self.assertIsNotNone(c.exit_time)
        self.assertGreater(c.exit_time, c.entry_time)

    def test_parked_duration_no_entry(self):
        """if car never entered, duration should be none"""
        c = Car("NULL1")
        self.assertIsNone(c.parked_duration())

    def test_parked_duration_without_exit(self):
        c = Car("LIVE1")
        c.record_entry()
        time.sleep(0.02)
        duration = c.parked_duration()
        self.assertGreater(duration, 0)

    def test_parked_duration_with_exit(self):
        """if car entered and exited, duration should be correct"""
        c = Car("DONE1")
        c.record_entry()
        time.sleep(0.02)
        c.record_exit()
        duration = c.parked_duration()
        expected = c.exit_time - c.entry_time

        self.assertAlmostEqual(duration, expected, delta = 0.001)

if __name__ == "__main__":
    unittest.main()