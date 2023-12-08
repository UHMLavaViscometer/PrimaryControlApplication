# Michael Dodge II
# ME 482: Senior Design Project (Fall 2023)
# Team Lava
import os # For shutting down the Raspberry Pi
import json # For parsing the JSON data from the Arduino
from datetime import datetime, timedelta # For adding timestamps
from papirus import PapirusText # For controlling the e-ink display
from serial import Serial # For communicating with the Arduino
import subprocess
from run_types import VerboseRunData, TerseRunData
from viscometer_equations import computeTorqueFrom10Bit, computeViscosityFromTorque, computeTemperatureFrom10Bit
from write_run_to_csv import write_run_to_csv
from make_eink_screen_content import make_content
from soft_update_display import soft_update_display

# Set up the PapirusText object
text = PapirusText()

# Set up the Serial object
ser = Serial('/dev/ttyACM0', 38400)

current_run_data: list[VerboseRunData] = []
current_terse_run_data: list[TerseRunData] = []
experiment_is_running = False
time_since_last_update = datetime.now()

text.write("Viscometer starting...")
text.write("")


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
    key_replacements = {
        'c': 'polling_cycles',
        't': 'time_since_power_on__ms',
        'gb': 'green_button_is_pressed',
        'rb': 'red_button_is_pressed',
        'sdb': 'shutdown_button_is_pressed',
        'tq': 'torque_raw_10bit',
        'tm': 'temperature_raw_10bit'
        }
    # Read the bytes from the serial port
    current_line_raw: bytes = ser.readline()
    # Decode the bytes into a string
    current_line_decoded: str = current_line_raw.decode('utf-8')
    # Parse the string as JSON
    try:
        current_line_data: dict = json.loads(current_line_decoded)
        temp = {key_replacements.get(k, k): v for k, v in current_line_data.items()}
        current_line_data = temp
    except:
        print("A bad line was received from the Arduino.")
    
    

    # Compute values and append the line to the current run data
    if experiment_is_running:
        # Calculate torque
        torque_calculated = computeTorqueFrom10Bit(current_line_data['torque_raw_10bit'])
        
        # Calculate viscosity
        viscosity_calculated = computeViscosityFromTorque(torque_calculated, 'newtonian')

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
            temperature_calculated = temperature_calculated,
            gps_lat = "to_be_implemented",
            gps_long = "to_be_implemented"
        )
        current_run_data.append(current_line_VerboseRunData)

        current_line_TerseRunData = TerseRunData(
            time = current_line_data["time_since_power_on__ms"],
            viscosity_calculated = viscosity_calculated,
            temperature_calculated = temperature_calculated,
            gps_lat = "to_be_implemented",
            gps_long = "to_be_implemented"
        )
        current_terse_run_data.append(current_line_TerseRunData)

    # Print the JSON object to the console
    print(current_line_data)


    ### Begin semi-cursed implemention of asynchronous display updating ###
    #time_since_last_update = soft_update_display(time_since_last_update, eink_content)
    # write current_line_data to a file, where it can be read by soft_update_display.py
    # the file name/location will be /tmp/viscometer_data_x.json where x is the cycle number
    if datetime.now() - time_since_last_update > timedelta(seconds=1):
        time_since_last_update = datetime.now()
        with open(f"/tmp/viscometer_data_{current_line_data['polling_cycles']}.json", 'w') as file:
            json.dump(current_line_data, file)
        subprocess.Popen(["python3", "./soft_update_display.py", f"/tmp/viscometer_data_{current_line_data['polling_cycles']}.json"])


    ### End semi-cursed implementation of asynchronous display updating ###

    # if the red button is pressed, stop logging data and write data
    if current_line_data["red_button_is_pressed"]:
        experiment_is_running = False
        try:
            write_run_to_csv(mode="verbose", data=VerboseRunData, base_dir="/dev/sda1")
        except Exception as e:
            print("Unable to write file to flash drive. Is it plugged in?")
            print(e)
        text.write("Run stopped.\n")

    # if the green button is pressed and a run isn't currently in progress, start
    if experiment_is_running is False and current_line_data["green_button_is_pressed"]:
        experiment_is_running = True
        experiment_start_time = datetime.now()
        text.write("")


    # if the shutdown button is pressed, signal to the operating system to shut down.
    # if current_line_data['sdb'] is True:
    #     text.write('Shutting down...')
    #     os.system('sleep 1 && shutdown -t 3 now')
    #     text.write("")
    #     break
    