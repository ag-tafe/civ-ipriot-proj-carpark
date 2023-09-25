if __name__ != '__main__':
    from no_pi import WindowedDisplay
    import threading
    import time
    import paho.mqtt.client as mqtt

class CarParkDisplay:
    """Provides a simple display of the car park status. This is a skeleton only. The class is designed to be customizable without requiring and understanding of tkinter or threading."""
    # determines what fields appear in the UI
    fields = ['Available bays', 'Temperature', 'At']

    def __init__(self, configuration: dict):
        self.initialize_values(configuration)
        self.initialize_mqtt()

        self.window = WindowedDisplay(
            self.location, CarParkDisplay.fields)

        updater = threading.Thread(target=self.check_updates)
        updater.daemon = True
        updater.start()
        self.window.show()

    def check_updates(self):
        # TODO: This is where you should manage the MQTT subscription

        while True:
            if self.firstrun == False:
                self.client.loop_start()  # Start the client loop to process network traffic
                while self.loopflag == True:   # wait on updates from MQTT
                    time.sleep(1)

                self.loopflag = True
            else:
                time.sleep(1)       # 1 second break on the first run to fill in values
            self.firstrun = False

            # NOTE: Dictionary keys *must* be the same as the class fields
            field_values = dict(zip(CarParkDisplay.fields, [
                f'{self.available_bays:03d}',
                f'{self.temperature:02d}℃',
                time.strftime("%H:%M:%S")]))

            # refresh the display.
            self.window.update(field_values)

    def on_message(self, client, userdata, message) -> None:
        """Executes when a message is received (https://pypi.org/project/paho-mqtt/#callbacks).

        Parameters
        ----------
        client :
            the client instance for this callback (not used)

        userdata :
             the private user data as set in Client() or user_data_set()  (not used)

        message :
            an instance of MQTTMessage. This is a class with members topic, payload, qos, retain.

        Returns
        ----------
            None.
        """

        decoded_message = str(message.payload.decode("utf-8"))
        print(time.strftime("%H:%M:%S"), self.client_id, " got a message from broker:", decoded_message)
        if decoded_message == "car goes in":
            if self.available_bays > 0:
                self.available_bays -= 1
            else:
                print("Sorry the car park is full!")
        elif decoded_message == "car goes out":
            if self.bays != self.available_bays:
                self.available_bays += 1
            else:
                print("No car can exit an empty car park!")

        if decoded_message.startswith("temp: "):
            self.temperature = int(decoded_message.split(": ")[1])
            print(f"Set the temperature on display to {self.temperature}")

        self.loopflag = False

    def initialize_values(self, configuration: dict) -> None:
        """Initializes car park instance with values from configuration dictionary

        Parameters
        ----------
        configuration : dict
            dictionary with keys-values for location, total_spaces, broker_host, broker_port.

        Returns
        ----------
            None.
        """
        self.location = configuration['location']
        self.bays = configuration["total_spaces"]
        self.server_host = configuration["broker_host"]
        self.server_port = configuration["broker_port"]
        self.available_bays = self.bays
        self.temperature = 20

    def initialize_mqtt(self) -> None:
        '''Initialize mqtt client'''
        self.loopflag = True
        self.firstrun = True
        self.client_id = self.location + " display"
        self.client = mqtt.Client(self.client_id)
        host = self.server_host
        port = self.server_port
        self.client.on_connect = self.on_connect
        try:
            self.client.connect(host, port)
        except ConnectionRefusedError:
            print(f"No connection could be made by {self.client_id} because the target machine {host} actively refused it")
            quit()
        except:
            print(f"Error! Unknown error occurred when establishing connection from {self.client_id} to {host} on port {port}")
            quit()

        self.client.subscribe(self.location)  # Subscribe to a topic to receive messages
        self.client.on_message = self.on_message  # Assign the callback function to the client


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
        ----------
            None.
        """
        if rc == 0:
            print(time.strftime("%H:%M:%S"), self.client_id, end=' ')
            print(f'connected to {self.server_host} on port {self.server_port}')
