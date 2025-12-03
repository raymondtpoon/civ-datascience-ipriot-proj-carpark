import unittest
import time
import os
from smartpark.manager import CarparkManager


class TestCarparkManager(unittest.TestCase):
    def setUp(self):
        """Run before every test"""
        self.manager = CarparkManager(total_spaces = 5)
        self.manager.log_file = "test_carpark.log"
        self.manager.total_spaces = 3
        self.manager.available = 3
        self.manager.cars_inside = {}

        # clean test log file before every test
        if os.path.exists("test_carpark.log"):
            os.remove("test_carpark.log")

    def tearDown(self):
        """Remove test log file after tests"""
        if os.path.exists("test_carpark.log"):
            os.remove("test_carpark.log")
    
    def test_incoming_car_success(self):
        """Car should enter and reduce available spaces"""
        self.manager.incoming_car("ABC123")

        self.assertIn("ABC123", self.manager.cars_inside)
        self.assertEqual(self.manager.available_spaces, 2)
    
    def test_prevent_negative_spaces(self):
        """No more cars allowed once full, available must remain 0."""
        self.manager.incoming_car("CAR1")
        self.manager.incoming_car("CAR2")
        self.manager.incoming_car("CAR3")

        # now carpark is full
        self.assertEqual(self.manager.available_spaces, 0)

        # 4th car should be rejected
        self.manager.incoming_car("CAR4")
        self.assertEqual(self.manager.available_spaces, 0) # still 0
        self.assertNotIn("CAR4", self.manager.cars_inside)

    def test_reject_empty_license_plate(self):
        """Empty or blank license plate should be rejected."""
        self.manager.incoming_car("")
        self.manager.incoming_car("   ")

        self.assertEqual(self.manager.available_spaces, 3)
        self.assertEqual(len(self.manager.cars_inside), 0)

    def test_outgoing_car_success(self):
        """Car exits successfully and frees a space"""
        self.manager.incoming_car("XYZ999")
        self.manager.outgoing_car("XYZ999")

        self.assertNotIn("XYZ999", self.manager.cars_inside)
        self.assertEqual(self.manager.available_spaces, 3)

    def test_unrecognised_car_exit(self):
        """a car not inside should NOT affect available spaces"""
        before = self.manager.available_spaces
        self.manager.outgoing_car("DOESNOTEXIST")
        after = self.manager.available_spaces

        self.assertEqual(before, after)

    def test_temperature_updates(self):
        """temperature updates and returns from property"""
        self.manager.temperature_reading(27.5)
        self.assertEqual(self.manager.temperature, 27)

        self.manager.temperature_reading(32)
        self.assertEqual(self.manager.temperature, 32)

    if __name__ == "__main__":
        unittest.main()