if __name__ != '__main__':
    from no_pi import WindowedDisplay, parse_config
    import threading
    import random
    import time
    import paho.mqtt.client as mqtt

class CarParkDisplay:
    """Provides a simple display of the car park status. This is a skeleton only. The class is designed to be customizable without requiring and understanding of tkinter or threading."""
    # determines what fields appear in the UI
    fields = ['Available bays', 'Temperature', 'At']

    def __init__(self):
        self.configuration = parse_config()
        self.location = self.configuration['location']
        self.bays = self.configuration["total_spaces"]
        self.available_bays = self.bays
        self.window = WindowedDisplay(
            self.location, CarParkDisplay.fields)

        self.client_id = self.location + " display"
        self.client = mqtt.Client(self.client_id)

        updater = threading.Thread(target=self.check_updates)
        updater.daemon = True
        updater.start()
        self.window.show()

    def check_updates(self):
        # TODO: This is where you should manage the MQTT subscription
        host = self.configuration["broker_host"]
        port = self.configuration["broker_port"]
        self.client.connect(host, port)
        print(f"{self.client_id} connected to {host} on port {port}")
        self.client.subscribe(self.location)  # Subscribe to a topic to receive messages
        self.client.on_message = self.on_message  # Assign the callback function to the client
        self.client.loop_start()  # Start the client loop to process network traffic

        while True:
            # NOTE: Dictionary keys *must* be the same as the class fields
            field_values = dict(zip(CarParkDisplay.fields, [
                f'{self.available_bays:03d}',
                f'{random.randint(0, 45):02d}℃',
                time.strftime("%H:%M:%S")]))
            # Pretending to wait on updates from MQTT
            time.sleep(random.randint(1, 10))
            # When you get an update, refresh the display.
            self.window.update(field_values)

    def on_message(self, client, userdata, message):
        # CarParkDisplay.fields[]
        decoded_message = str(message.payload.decode("utf-8"))
        print(time.strftime("%H:%M:%S"), self.client_id, " got a message from broker: ", decoded_message)
        if decoded_message == "car goes in":
            if self.available_bays > 0:
                self.available_bays -= 1
            else:
                print("Sorry the car park is full!")
        elif decoded_message == "car goes out":
            if self.bays != self.available_bays:
                self.available_bays += 1
        else:
            print("Error! Unknown message received!")


