if __name__ != '__main__':
    import tkinter as tk
    import time
    import paho.mqtt.client as mqtt
    import random
    import sys


class Sensor:
    """Provides random temperature"""
    def __init__(self):
        """Initialize by 20 degrees Celsius."""
        self.temperature = 20

    def read_temperature(self) -> int:
        """Get a random temperature value (20-32)."""
        self.temperature = random.randint(20, 33)
        return self.temperature

class CarDetector:
    """Provides a couple of simple buttons that can be used to represent a sensor detecting a car. This is a skeleton only."""

    def __init__(self, configuration: dict):
        self.initialize_values(configuration)
        self.initialize_mqtt()
        self.sensor = Sensor()


        self.root = tk.Tk()
        self.root.title("Car Detector ULTRA")

        self.btn_incoming_car = tk.Button(
            self.root, text='🚘 Incoming Car', font=('Arial', 50), cursor='right_side', command=self.incoming_car)
        self.btn_incoming_car.pack(padx=10, pady=5)
        self.btn_outgoing_car = tk.Button(
            self.root, text='Outgoing Car 🚘',  font=('Arial', 50), cursor='bottom_left_corner', command=self.outgoing_car)
        self.btn_outgoing_car.pack(padx=10, pady=5)

        self.root.mainloop()

    def incoming_car(self) -> None:
        """Sends messages via MQTT about car going in with temperature and time values."""
        print("Car goes in")
        temperature = self.sensor.read_temperature()
        time_stamp = time.strftime("%H:%M:%S")
        self.client.publish(self.location, "car goes in")
        self.client.publish(self.location, f"temp: {temperature}")
        self.client.publish(self.location, f"time: {time_stamp}")

    def outgoing_car(self) -> None:
        """Sends messages via MQTT about car going out with temperature and time values."""
        print("Car goes out")
        temperature = self.sensor.read_temperature()
        time_stamp = time.strftime("%H:%M:%S")
        self.client.publish(self.location, "car goes out")
        self.client.publish(self.location, f"temp: {temperature}")
        self.client.publish(self.location, f"time: {time_stamp}")

    def on_connect(self, client, userdata, flags, rc) -> None:
        """Called when the broker responds to our connection request. https://pypi.org/project/paho-mqtt/#callbacks

            Parameters
            ----------
                client
                    the client instance for this callback (not used)

                userdata
                    the private user data as set in Client() or user_data_set() (not used)

                flags
                    response flags sent by the broker (not used)

                rc
                    the connection result. 0 means the connection was successful.

            Returns
                None.
        """
        if rc == 0:
            print(time.strftime("%H:%M:%S"), self.client_id, end=' ')
            print(f'connected to {self.server_host} on port {self.server_port}', end=' ')


    def initialize_values(self, configuration: dict) -> None:
        """Initialize car park with values from configuration dictionary.
        Parameters
            configuration: dict
                dictionary with keys-values for location, total_spaces, broker_host, broker_port.

        Returns
            None.
        """
        self.location = configuration['location']
        self.server_host = configuration["broker_host"]
        self.server_port = configuration["broker_port"]

    def initialize_mqtt(self) -> None:
        """Initialize mqtt client
        Parameters
            None

        Returns
            None.
        """
        self.client_id = self.location + " car detector"
        self.client = mqtt.Client(self.client_id)
        host = self.server_host
        port = self.server_port
        self.client.on_connect = self.on_connect
        try:
            self.client.connect(host, port)
        except ConnectionRefusedError:
            print(f"No connection could be made by {self.client_id} because the target machine {host} actively refused it")
            sys.exit(1)
        self.client.loop_start()