# Michael Dodge II
# ME 482: Senior Design Project (Fall 2023)
# Team Lava
import os # For shutting down the Raspberry Pi
import json # For parsing the JSON data from the Arduino
import datetime # For adding timestamps
from papirus import PapirusText # For controlling the e-ink display
from serial import Serial # For communicating with the Arduino
from run_types import VerboseRunData, TerseRunData
from viscometer_equations import computeTorqueFrom10Bit, computeViscosityFromTorque, computeTemperatureFrom10Bit

# Set up the PapirusText object
text = PapirusText()

# Set up the Serial object
ser = Serial('/dev/ttyACM0', 38400)

current_run_data: list(VerboseRunData) = []
experiment_is_running = False

while True:
    # Read the JSON object that the Arduino sends.
    # The JSON object is a dictionary.
    # The dictionary contains the following keys:
    # unsigned 32-bit int c: the amount of cycles since the start of the run
    # float t: the amount of time since the start of the operational period
    # int gb: the boolean state of the digital pin for the green button
    # int rb: the boolean state of the digital pin for the red button
    # int sdb: the boolean state of the digital pin for the shutdown button
    # int tq: the raw analog (0-1023) value of the torque sensor
    # int tm: the raw analog (0-1023) value of the temperature sensor

    # The Arduino sends the JSON object as utf-8 encoded bytes.
    # We need to decode the bytes into a string, then parse the string as JSON.

    # Read the bytes from the serial port
    current_line_raw: bytes = ser.readline()
    # Decode the bytes into a string
    current_line_decoded: str = current_line_raw.decode('utf-8')
    # Parse the string as JSON
    current_line_data: dict = json.loads(current_line_decoded)
    key_replacements = {
        'c': 'polling_cycles',
        't': 'time_since_power_on__ms',
        'gb': 'green_button_is_pressed',
        'rb': 'red_button_is_pressed',
        'sdb': 'shutdown_button_is_pressed',
        'tq': 'torque_raw_10bit',
        'tm': 'temperature_raw_10bit'
        }
    temp = {key_replacements.get(k, k): v for k, v in current_line_data.items()}
    current_line_data = temp

    # Compute values and append the line to the current run data
    if experiment_is_running:
        # Calculate torque
        torque_calculated = computeTorqueFrom10Bit(current_line_data['torque_raw__10bit'])
        
        # Calculate viscosity
        viscosity_calculated = computeViscosityFromTorque(torque_calculated)

        # Calculate temperature
        temperature_calculated = computeTemperatureFrom10Bit(current_line_data['temperature_raw_10bit'])

        # Create a VerboseRunData object
        current_line_VerboseRunData = VerboseRunData(
            cycles = current_line_data['polling_cycles'],
            time = current_line_data['time_since_power_on__ms'],
            green_button = current_line_data['green_button_is_pressed'],
            red_button = current_line_data['red_button_is_pressed'],
            shutdown_button = current_line_data['shutdown_button_is_pressed'],
            torque_raw_10bit = current_line_data['torque_raw_10bit'],
            torque_calculated = torque_calculated,
            viscosity_calculated = viscosity_calculated,
            temperature_raw_10bit = current_line_data['temperature_raw_10bit'],
            temperature_calculated = temperature_calculated
        )
        current_run_data.append(current_line_VerboseRunData)

    # Print the JSON object to the console
    print(current_line_data)


    # if the red button is pressed, stop logging data
    if current_line_data["red_button_is_pressed"]:
        experiment_is_running = False

    # if the green button is pressed and a run isn't currently in progress, start
    if experiment_is_running is False and current_line_data["green_button_is_pressed"]:
        experiment_is_running = True
        experiment_start_time = datetime.now()


    # if the shutdown button is pressed, signal to the operating system to shut down.
    # if current_line_data['sdb'] is True:
    #     text.write('Shutting down...')
    #     os.system('sleep 1 && shutdown -t 3 now')
    #     text.write("")
    #     break
    