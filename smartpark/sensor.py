from sense_emu import SenseHat


### Class: Sensor
class Sensor:
    def __init__(self):
        """Initialize the Sensor object with a SenseHAT instance."""
        self.sense_hat = SenseHat() # The SenseHAT object to control the sensors.
        self.sense_hat.stick.direction_up = handle_joystick

    def read_temperature(self):
        """Read the temperature from the SenseHAT sensor."""
        return self.sense_hat.get_temperature()

    def handle_joystick(event):
        if event.action == "pressed" and event.direction == "up":
            # send message to parking lot??? display???
            pass



if __name__ == '__main__':
    a = Sensor()