# Michael Dodge II
# ME 482: Senior Design Project (Fall 2023)
# Team Lava
import io
import csv
import os
from run_types import VerboseRunData, TerseRunData
from typing import Union

def write_run_to_csv(mode: str, data: Union[list[VerboseRunData], list[TerseRunData]]) -> str:
    """Writes an experiment run to a CSV on the local filesystem.\n
    It names the file using ISO 8601 conventions\n
    Example: viscometer_2023-11-01T13:19:02-10:00.csv"""
    
    os.path.abspath()