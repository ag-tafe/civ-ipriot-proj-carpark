# IPRIoT Project: Simulated Workplace Scenario

A simulated workplace environment where to demonstrate OO skills by interpreting and interacting with modern software requirements.

## Description

This is an implementation of the car park project without using Raspberri PI.


## How to run

1. Clone the project onto your computer using 
```bash
git clone
```
2. Change to the cloned repository's directory:
```bash
cd civ-ipriot-proj-carpark
```
3. Create virtual environment 
```bash
python3 -m venv .venv
```
Then activate the virtual environment:
- On Linux/macOS:
```bash
source .venv/bin/activate
```
- On Windows:
```bash
.venv\Scripts\activate
```
4. Install the SmartPark project in development mode using:
```bash
pip install -e .
```
5. Navigate to "without_pi" directory using cd command
```bash
cd without_pi
```
The folder contents are listed below.
You'll need to make sure mqtt broker service is running on default port (1883) on localhost or update "toml_no_pi_configuration.toml" accordingly.
Run "main01.py" and run "main02.py"
at the same time e.g.
```bash
python3 main01.py
```
```bash
python3 main02.py
```
The directory contents:
```text
│
├── without_pi/
│   ├── main01.py           <-- run this
│   ├── main02.py       <-- and that
│   ├── requirements.txt           <-- project dependencies
│   ├── car_detector.py      <-- classes CarDetector, Sensor
│   ├── car_park_display.py  < -- class CarParkDisplay
│   ├── test_config.py       <-- unit test
│   └── toml_no_pi_configuration.toml <-- toml configuration
```

- **`main01.py`**: Reads the configuration file and passes dictionary to the classes initializers. The window has 2 buttons for incoming and outgoing cars.
 Once the user clicks on either button a random temperature value, time stamp and the fact that a car has entered or exited the car park are sent via MQTT protocol.   
- **`main02.py`**: This is a "screen" with information for a car park manager or a car park user. This window receives data via MQTT protocol and updates available bays, temperature, last update time and current time. 

## Test
Run test_config.py
