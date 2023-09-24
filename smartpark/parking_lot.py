import paho.mqtt.client as mqtt

### Class: ParkingLot
class ParkingLot:
    '''The parking lot reports its state to display'''

    def __init__(self, config):
        """Initialize the ParkingLot object with the given configuration."""
        """The parking lot's location."""
        self.location = config["location"]
        """The total number of parking spaces."""
        self.total_spaces = config["total_spaces"]
        """The number of available parking spaces."""
        self.available_spaces = config["total_spaces"] // 2
        """The MQTT client to send and receive messages."""
        self.mqtt_client = mqtt.Client()  # Create an MQTT client instance
        self.mqtt_client.connect(config["broker_host"], config["broker_port"])  # Connect the client to the MQTT broker using the provided host and port
        self.mqtt_client.subscribe("topic_name") # Subscribe to a topic to receive messages
        self.mqtt_client.on_message = self.on_message # Assign the callback function to the client
        self.mqtt_client.loop_start() # Start the client loop to process network traffic

    def enter(self):
        """Register a car entering the parking lot."""
        print("Car entering...")

    def exit(self):
        """Register a car leaving the parking lot."""
        print("Car exiting...")

   def publish_update(self):
       """Publish an update containing available_spaces, temperature, and time."""
       #self.mqtt_client
       pass

   def on_message(client, userdata, message):
       """Callback function to handle received messages."""
       pass

