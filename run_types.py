# Michael Dodge II
# ME 482: Senior Design Project (Fall 2023)
# Team Lava
class VerboseRunData:
    """Contains the full details of the run, intended for debugging purposes."""
    def __init__(
            self, 
            cycles: int, 
            time: int, 
            green_button: bool,
            red_button: bool,
            shutdown_button: bool,
            torque_raw_10bit: int,
            torque_calculated: float,
            viscosity_calculated: float,
            temperature_raw_10bit: int,
            temperature_calculated: float,
            gps_lat: str,
            gps_long: str):
        self.cycles = cycles
        self.time = time
        self.green_button = green_button
        self.red_button = red_button
        self.shutdown_button = shutdown_button
        self.torque_raw_10bit_5volt = torque_raw_10bit
        self.torque_calculated = torque_calculated
        self.viscosity_calculated = viscosity_calculated
        self.temperature_raw_10bit_5volt = temperature_raw_10bit
        self.temperature_calculated = temperature_calculated
        self.gps_lat = gps_lat
        self.gps_long = gps_long


class TerseRunData:
    """Contains the necessary variables of the run, intended for typical analysis."""
    def __init__(
            self,
            time: int,
            viscosity_calculated: float,
            temperature_calculated: float,
            gps_lat: str,
            gps_long: str):
        self.time = time,
        self.viscosity_calculated = viscosity_calculated,
        self.temperature_calculated = temperature_calculated,
        self.gps_lat = gps_lat,
        self.gps_long = gps_long