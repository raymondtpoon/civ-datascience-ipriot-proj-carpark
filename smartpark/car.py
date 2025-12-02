
import time
####
"""
    - The "display" should update instantly when something happens
    - Make a "Car" class to contain information about cars:
        * License plate number. You can use this as an identifier
        * Entry time
        * Exit time
"""


class Car:
    """
    Represents each car in the carpark

    Attributes
    ----------
    license_plate: str
        license plate no. of the car    
    entry_time: float
        time of entry of car
    exit_time: float
        time of exit of car
    """
    def __init__(self,plate = None):
        """
        Initialising a new Car instance

        Parameters
        ----------
        plate: str, optional
            The license plate number of the car (default is none)
        """
        self.license_plate = plate
        self.entry_time = None
        self.exit_time = None

    def record_entry(self):
        """
        Records the entry time of the car as the current time.
        """
        self.entry_time = time.time()

    def record_exit(self):
        """
        Records the exit time of the car as the current time.
        """
        self.exit_time = time.time()

    def parked_duration(self):
        """
        Calculates total duration of car being parked.

        Returns
        -------
        float or None
            The time between entry and exit, if the car hasn't entered yet it will return None. 
            If the car has entered but not exited will calculate the duration up till current time. 
        """
        if self.entry_time is None:
            return None
        end_time = self.exit_time or time.time() # provides duration of car parked inside even if it hasnt exited
        return end_time - self.entry_time

# creating instance of car class 
my_car = Car(plate="ABC123")

# checking initial values 
print(my_car.license_plate)
print(my_car.entry_time)
print(my_car.exit_time)

# record entry
my_car.record_entry()
print("Entry time:", my_car.entry_time)