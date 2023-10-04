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
You'll need to run "run_car_detector.py" and run "run_car_park_display.py"
at the same time
```text
│
├── without_pi/
│   ├── run_car_detector.py           <-- run this
│   ├── run_car_park_display.py       <-- and that
│   ├── requirements.txt           <-- project dependencies
│   ├── car_detector.py      <-- classes CarDetector, Sensor
│   ├── car_park_display.py  < -- class CarParkDisplay
│   ├── test_config.py       <-- unit test
│   └── toml_no_pi_configuration.toml <-- toml configuration
```

- **`run_car_detector.py`**: Reads the configuration file and passes dictionary to the classes initializers. The window has 2 buttons for incoming and outgoing car.
 Once the user clicks on either button a random temperature value, time stamp and the fact that a car has entered or exited the car park are sent via MQTT protocol.   
- **`run_car_park_display.py`**: This is a "screen" with information for a car park manager or a car park user. This window receives data via MQTT protocol and updates available bays, temperature, last update time and current time. 

## Test
Run test_config.py
