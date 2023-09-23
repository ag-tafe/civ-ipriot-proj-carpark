from sense_emu import SenseHat


### Class: Sensor
class Sensor:
    def __init__(self):
        """Initialize the Sensor object with a SenseHAT instance."""
        self.sense_hat = SenseHat() # The SenseHAT object to control the sensors.

    def read_temperature(self):
        """Read the temperature from the SenseHAT sensor."""
        return self.sense_hat.get_temperature()

if __name__ == '__main__':
    a = Sensor()