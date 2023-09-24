if __name__ != '__main__':
    import tkinter as tk
    from no_pi import parse_config
    import time
    import paho.mqtt.client as mqtt

class CarDetector:
    """Provides a couple of simple buttons that can be used to represent a sensor detecting a car. This is a skeleton only."""

    def __init__(self, configuration):
        self.initialize_values(configuration)
        self.initialize_mqtt()


        self.root = tk.Tk()
        self.root.title("Car Detector ULTRA")

        self.btn_incoming_car = tk.Button(
            self.root, text='🚘 Incoming Car', font=('Arial', 50), cursor='right_side', command=self.incoming_car)
        self.btn_incoming_car.pack(padx=10, pady=5)
        self.btn_outgoing_car = tk.Button(
            self.root, text='Outgoing Car 🚘',  font=('Arial', 50), cursor='bottom_left_corner', command=self.outgoing_car)
        self.btn_outgoing_car.pack(padx=10, pady=5)

        self.root.mainloop()

    def incoming_car(self):
        # TODO: implement this method to publish the detection via MQTT
        print("Car goes in")
        self.client.publish(self.location, "car goes in")

    def outgoing_car(self):
        # TODO: implement this method to publish the detection via MQTT
        print("Car goes out")
        self.client.publish(self.location, "car goes out")

    def on_connect(self, client, userdata, flags, rc):
        print(time.strftime("%H:%M:%S"), self.client_id, end=' ')
        print(f'connected to {self.server_host} on port {self.server_port}', end=' ')
        print(f'Connected with result code {rc}')

    def initialize_values(self, configuration: dict) -> None:
        '''Initialize car park with values from configuration dictionary'''
        self.location = configuration['location']
        self.server_host = configuration["broker_host"]
        self.server_port = configuration["broker_port"]

    def initialize_mqtt(self) -> None:
        '''Initialize mqtt client'''
        self.client_id = self.location + " car detector"
        self.client = mqtt.Client(self.client_id)
        host = self.server_host
        port = self.server_port
        self.client.on_connect = self.on_connect
        self.client.connect(host, port)
        self.client.loop_start()