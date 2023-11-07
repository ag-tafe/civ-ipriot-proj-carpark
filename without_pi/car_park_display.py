if __name__ != '__main__':
    from main02 import WindowedDisplay
    import threading
    import time
    import sys
    import json
    import paho.mqtt.client as mqtt

class CarParkDisplay:
    """Provides a simple display of the car park status."""
    # determines what fields appear in the UI
    fields = ['Available bays', 'Temperature', 'Updated at', "Time"]

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
        # MQTT subscription is managed here

        while True:
            self.client.loop_start()
            time.sleep(0.5)

            # NOTE: Dictionary keys *must* be the same as the class fields
            field_values = dict(zip(CarParkDisplay.fields, [
                f'{self.available_bays:03d}',
                f'{self.temperature:02d}℃',
                f'{self.time}',
                f'{time.strftime("%H:%M:%S")}']))

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
        # convert dictionary string to dictionary
        # https://www.geeksforgeeks.org/python-convert-string-dictionary-to-dictionary/
        recevied_values = json.loads(decoded_message)

        for key, value in recevied_values.items():
            if key == 'available_bays':
                self.available_bays = value
            elif key == 'temperature':
                self.temperature = value
            elif key == 'time':
                self.time = value
            else:
                raise Exception("Unable to process key:", key)

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
        self.available_bays = configuration["total_spaces"]
        self.server_host = configuration["broker_host"]
        self.server_port = configuration["broker_port"]
        self.temperature = 20
        self.time = time.strftime("%H:%M:%S")

    def initialize_mqtt(self) -> None:
        '''Initialize mqtt client'''
        self.client_id = self.location + " display"
        self.client = mqtt.Client(self.client_id)
        host = self.server_host
        port = self.server_port
        self.client.on_connect = self.on_connect
        try:
            self.client.connect(host, port)
        except ConnectionRefusedError:
            print(f"No connection could be made by {self.client_id} because the target machine {host} actively refused it")
            sys.exit(1)

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
