# Michael Dodge II
# ME 482: Senior Design Project (Fall 2023)
# Team Lava
import numpy as np
from typing import Literal

def computeTorqueFrom10Bit(torque_10bit: int) -> float:
    """Converts the 10-bit integer digitization of the torque sensor's output to floating-point Newton-meters.\n
    Example: 100 -> 0.02 N-m\n
    Limits: 0-1023 -> 0-tau_max"""
    return 0.0 #TODO implement this

def computeViscosityFromTorque(torque_Nm: float, fluid_type: Literal["newtonian", "thixotropic"]) -> float:
    """Computes a viscosity value in cPs from the given torque, using the selected model."""
    if fluid_type == "newtonian":
        # TODO: Implement calculation for newtonian fluid
        return 0.0
    elif fluid_type == "thixotropic":
        # TODO: Implement calculation for thixotropic fluid
        return 0.0
    else:
        raise ValueError("Invalid fluid type. Must be 'newtonian' or 'thixotropic'")

def computeTemperatureFrom10Bit(temperature_10bit: int) -> float:
    """Converts the 10-bit integer digitization of the thermocouple DAC's output to floating-point Kelvin.\n
    Example: 500 -> 680 K\n
    Limits: 0-1023 -> 0-T_max"""
    return 0.0 #TODO implement this