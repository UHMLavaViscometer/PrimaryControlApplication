import io
import csv
import os
from run_types import VerboseRunData, TerseRunData
from typing import Union

def write_run_to_csv(mode: str, data: Union[list[VerboseRunData], list[TerseRunData]]) -> str:
    """"""
    
    os.path.abspath()