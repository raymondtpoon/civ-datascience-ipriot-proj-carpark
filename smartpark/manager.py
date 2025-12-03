from interfaces import CarparkSensorListener
from interfaces import CarparkDataProvider
from config_parser import parse_config
import time
from car import Car

'''
    TODO: 
    - make your own module, or rename this one. Yours won't be a mock-up, so "mocks" is a bad name here.
    - Read your configuration from a file. 
    - Write entries to a log file when something happens.
    - The "display" should update instantly when something happens
    - Make a "Car" class to contain information about cars:
        * License plate number. You can use this as an identifier
        * Entry time
        * Exit time
    - The manager class should record all activity. This includes:
        * Cars arriving
        * Cars departing
        * Temperature measurements.
    - The manager class should provide informtaion to potential customers:
        * The current time (optional)
        * The number of bays available
        * The current temperature
    
'''
class CarparkManager(CarparkSensorListener,CarparkDataProvider):
    """
    Manages the carpark by tracking incoming/outgoing cars, available spaces, temperature and time. The events which occur also get recorded in a log. 

    This class also provides data to the display system and responds to sensor events.
    """
    CONFIG_FILE = "samples_and_snippets/config.json"

    def __init__(self, total_spaces = None):
        """Initialises the CarparkManager instance by loading configuration, preparing log file and setting up storage for cars and temperature"""
        self.config = parse_config(CarparkManager.CONFIG_FILE) # self allows parsing style to be used 
        self.log_file = "carpark.log" # logs any events that occur 
        self.total_spaces = self.config["total_spaces"] # stores value of the key "total_spaces" from json file
        self.available = self.total_spaces 
        self.last_temperature = None
        self.cars_inside = {} # will use to track cars by license plate 
        
        print(">>> using my carpark manager <<<")
        print("logging to:", self.log_file)

    @property
    def available_spaces(self):
        """Provides number of parking spaces available by subtracting number of cars inside carpark from total spaces of the carpark.""" 
        return self.total_spaces - len(self.cars_inside)

    @property
    def temperature(self):
        """Provides current temperature to potential customers and is displated on the GUI, or will return last known temperature if no changes.
        
        If no temperature recorded yet it will return 0.
        """
        return int(self.last_temperature or 0) 

    @property
    def current_time(self):
        """Provides current time"""
        return time.localtime()

    def incoming_car(self, license_plate):
        """Manages a car with a license plate entering the carpark.

        Records entry time, updates available spaces, prevents entry if carpark is full and logs any of these events.

        Parameters:
            license_plate (str): This is the license plate number of the car entering
        """
        print('Car in! ' + license_plate)

        # only allows cars with license plates to enter
        if not license_plate or license_plate.strip() =="":
            print("Invalid entry: No license plate detected.")
            with open(self.log_file, "a") as f:
                f.write(f"FAILED ENTRY: Missing license plate at {time.ctime()}\n")
            return
        
        if self.available <= 0: # checks if carpark is full or not first, before admitting entry of cars (no negatives)
            print("Sorry, carpark is full at this time:", time.ctime())
            with open(self.log_file, "a") as f:
                f.write(f"FAILED ENTRY: Car {license_plate} attempted entry but carpark FULL at {time.ctime()}\n")
                f.write(f"Available spaces: {self.available_spaces}\n")
                f.write(f"Carpark temperature {self.last_temperature}\n")
            return

        car = Car(license_plate)
        car.record_entry()
        self.cars_inside[license_plate] = car        
        self.available -= 1 

        # displays info for driver
        print(f"Car {license_plate} entered at {time.ctime()}")
        print(f"Available spaces: {self.available_spaces}/{self.total_spaces}")
        print(f"Current temperature: {self.temperature}°C")

        # logs events
        with open(self.log_file, "a") as f:
            f.write(f"ENTRY: Car {license_plate} entered at {time.ctime()}\n")
            f.write(f"Available spaces: {self.available_spaces}/{self.total_spaces}\n")
            f.write(f"Carpark temperature {self.last_temperature}\n")
            f.write(f"Car {license_plate} entered at {time.ctime()}\n")
            return  

        # self.available -= 1

    def outgoing_car(self,license_plate):
        """
        Handles car exiting the carpark.

        Updates available spaces, logs the exit, and removes car from internal tracking. 

        Unrecognised cars are ignored.

        Parameters:
            license_plate (str): The license plate number of the car exiting.
        """
        print('Car out! ' + license_plate)
        
        # checks if car is actually inside carpark
        if license_plate not in self.cars_inside:
            print("Unrecognised car ignored.")
            with open(self.log_file, "a") as f:
                f.write(f"FAILED EXIT: Car {license_plate} not found inside carpark at {time.ctime()}\n")
                f.write(f"Available spaces: {self.available}/{self.total_spaces}\n")
                f.write(f"Carpark temperature: {self.last_temperature}\n")
            return
    
        # Remove car and update available spaces
        self.cars_inside[license_plate].record_exit()
        del self.cars_inside[license_plate]
        self.available += 1

        # Prevent exceeding total spaces
        if self.available > self.total_spaces:
            self.available = self.total_spaces

        # Display info for driver
        print(f"Car {license_plate} exited at {time.ctime()}")
        print(f"Available spaces: {self.available}/{self.total_spaces}")
        print(f"Current temperature: {self.temperature}°C")

        # Log successful exit
        with open(self.log_file, "a") as f:
            f.write(f"EXIT: Car{license_plate} exited at {time.ctime()}\n")
            f.write(f"Available spaces: {self.available}/{self.total_spaces}\n")
            f.write(f"Carpark temperature: {self.last_temperature}\n")
            f.write(f"Current time: {time.ctime()}\n")   

    def temperature_reading(self,reading):
        """Records new temperature reading and logs it.
        
        Parameters:
            reading (float or int): The temperature value provided by a simulated sensor. 
        """
        self.last_temperature = reading
        print(f'temperature is {reading}') 

        with open(self.log_file, "a") as f: # writes and appends ie adds temp reading to file
             f.write(f"Temperature reading: {reading} at {time.ctime()}\n")

    def count_cars_inside(self):
        """
        Returns number of cars currently inside the carpark.
        """
        return len(self.cars_inside)


test = parse_config(CarparkManager.CONFIG_FILE)
print("Parsing test \n-------------\n",test)

# manager = CarparkManager() 
# manager.incoming_car("TEST123")

# testing if program will count cars based on whether car removal and available spaces work
mgr = CarparkManager()

print("\n=== TEST: 1 car enters ===")
mgr.incoming_car("AAA111")
print("Cars inside:", mgr.count_cars_inside())
print("Available spaces:", mgr.available_spaces)

print("\n=== TEST: same car exits ===")
mgr.outgoing_car("AAA111")
print("Cars inside:", mgr.count_cars_inside())
print("Available spaces:", mgr.available_spaces)
