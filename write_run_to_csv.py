# Michael Dodge II
# ME 482: Senior Design Project (Fall 2023)
# Team Lava
import io
import csv
import os
from datetime import datetime
from run_types import VerboseRunData, TerseRunData
from typing import Union

def write_run_to_csv(mode: str, data: Union[list[VerboseRunData], list[TerseRunData]], base_dir: str) -> str:
    """Writes an experiment run to a CSV on the local filesystem.\n
    It names the file using ISO 8601 conventions\n
    Example: viscometer_2023-11-01T13:19:02.csv"""

    # Get timestamp
    timestamp: str = datetime.now().replace(microsecond=0).isoformat()
    filename: str = f"{base_dir}/viscometer_{timestamp}"

    if mode is "verbose":
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = [
                'Arduino Cycles Since Power-on', 
                'Time [ms]', 
                'Green Button Is Pressed', 
                'Red Button Is Pressed', 
                'Shutdown Button',
                'Torque (Raw 10-bit)',
                'Torque (Calculated) [N*m]',
                'Viscosity (Calculated) [mPa*s]',
                'Temperature (Raw 10-bit)',
                'Temperature (Calculated) [K]',
                'GPS Latitude [deg.deci]',
                'GPS Longitude [deg.deci]'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for datapoint in data:
                writer.writerow({
                    'Arduino Cycles Since Power-on': datapoint.cycles, 
                    'Time [ms]': datapoint.time, 
                    'Green Button Is Pressed': datapoint.green_button, 
                    'Red Button Is Pressed': datapoint.red_button, 
                    'Shutdown Button': datapoint.shutdown_button,
                    'Torque (Raw 10-bit)': datapoint.torque_raw_10bit_5volt,
                    'Torque (Calculated) [N*m]': datapoint.torque_calculated,
                    'Viscosity (Calculated) [mPa*s]': datapoint.viscosity_calculated,
                    'Temperature (Raw 10-bit)': datapoint.temperature_raw_10bit_5volt,
                    'Temperature (Calculated) [K]': datapoint.temperature_calculated,
                    'GPS Latitude [deg.deci]': datapoint.gps_lat,
                    'GPS Longitude [deg.deci]': datapoint.gps_long 
                })
    if mode is "terse":
        with open(filename, 'w', newline='') as csvfile:
            fieldnames =[
                'Time [ms]',
                'Viscosity [mPa*s]',
                'Temperature [K]',
                'GPS Lat [deg.deci]',
                'GPS Long [deg.deci]'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for datapoint in data:
                writer.writerow({
                    'Time [ms]': datapoint.time,
                    'Viscosity [mPa*s]': datapoint.viscosity_calculated,
                    'Temperature [K]': datapoint.temperature_calculated,
                    'GPS Lat [deg.deci]': datapoint.gps_lat,
                    'GPS Long [deg.deci]': datapoint.gps_long
                })
    return filename