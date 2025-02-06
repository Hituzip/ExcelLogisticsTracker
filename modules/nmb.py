import os
from typing import Union
import pandas as pd

from modules.excel_parser import parse_float

def nmb_column_sum(file: Union[str, os.PathLike]) -> list:
    """Суммирует данные из определённых столбцов нескольких листов Excel."""
    df = pd.read_excel(file, sheet_name=[1, 2, 4], skiprows=1, dtype=str)
    
    take = sum(map(parse_float, df[1][42].values))
    out = sum(map(parse_float, df[2][42].values))
    stay = sum(map(parse_float, df[4][21].values))

    return [take, out, stay]